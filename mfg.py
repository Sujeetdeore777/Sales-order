from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class Mfg(models.Model):
    _name = 'sales_order_system.mfg'
    _description = 'mfg'
    
    sales_order_ = fields.Many2one('sales_order_system.sales_order', string='Sales Order')
    item_rate_ = fields.Many2one(related='sales_order_.item_rate_.item_', string='Item Rate')
    date = fields.Date(string='Date')  
    qty = fields.Integer(string='Quantity')
    
    _rec_name = "sales_order_"

    @api.onchange('qty')
    def check_manufacturing_quantity(self):
        for mfg in self:
            if mfg.qty > mfg.sales_order_.qty or mfg.sales_order_.bal_to_mfg < 0:
                raise ValidationError("Manufacturing quantity cannot be greater than the quantity in the sales order or the balance to manufacture is less than 0.")
   
    @api.onchange('item_rate_')
    def onchange_item(self):
        if self.item_rate_:
            sale_orders = self.env['sales_order_system.sales_order'].search([('so_code', '=', self.sales_order_.so_code)])
            if sale_orders:
                self.sales_order_ = sale_orders[0]

  
 

# transion model mfg
class Tmfg(models.TransientModel):
    _name = 'sales_order_system.tmfg'
    
    sales_order_ = fields.Many2one('sales_order_system.sales_order', string='Sales Order')
    item_rate_ = fields.Many2one(related='sales_order_.item_rate_.item_', string='Item Rate')
    date = fields.Date(string='Date', default=lambda self: fields.Date.today())  
    qty = fields.Integer(string='Quantity')
    
  
    
    def genbook(self):
        if self.qty > self.sales_order_.qty or self.sales_order_.bal_to_mfg < 0:
            raise UserError("Manufacturing quantity cannot be greater than the quantity in the sales order or the balance to manufacture is less than 0.")
        bo = self.env[ 'sales_order_system.mfg' ].create( {
                                    'sales_order_': self.sales_order_.id ,
                                    'item_rate_': self.item_rate_,
                                    'qty': self.qty,
                                    'date': self.date,
                                    } )
        return True
        
        
        
    # @api.onchange('qty')
    # def check_manufacturing_quantity(self):
    #     for mfg in self:
            

    # @api.onchange('sales_order_')
    # def onchange_item(self):
    #     if self.sales_order_:
    #         # sale_orders = self.env['miniproj.saleorders'].search([('item_rate_.item_', '=', self.item_.id)])
    #         sale_orders = self.env['sales_order_system.sales_order'].search([('so_code', '=', self.sales_order_.so_code)])
    #         if sale_orders:
    #             self.sales_order_ = sale_orders[0]