import datetime
from odoo import api, fields, models, exceptions
from datetime import date  # Import the date class from the datetime module
from odoo.exceptions import ValidationError,UserError

import logging
_logger = logging.getLogger(__name__)

# class department():
    # descrip....
    # editable tree view

class Dispatch(models.Model):
    _name = 'sales_order_system.dispatch'
    _description = 'dispatch'
    
    dispatch_date = fields.Date(string='Dispatch Date')  
    sales_order_ = fields.Many2one('sales_order_system.sales_order', string='Sales Order')
    customer_master_ = fields.Many2one(related='sales_order_.cutomer_', string='Customer Name')
    item_ = fields.Many2one(related='sales_order_.item_rate_.item_', string='Item Rate')
    qty = fields.Integer(string='Quantity')
    agree_rate = fields.Text(related='sales_order_.item_rate_.agree_rate', string='Rate')
    amount = fields.Float(string='Amount', compute="_compute_amount")
    
    _rec_name = "sales_order_"
    
    
    @api.depends('qty')
    def _compute_amount(self):
        logger = logging.getLogger(__name__)

        for dispatch_record in self:
            try:
                agree_rate = float(dispatch_record.agree_rate or 0)
                amount = dispatch_record.qty * agree_rate
                dispatch_record.amount = amount
                logger.info(f"Computed amount for Dispatch {dispatch_record.id}: {amount}")
            except ValueError:
                logger.error(f"Invalid agree_rate value for Dispatch {dispatch_record.id}: {dispatch_record.agree_rate}")

        return True
                
    @api.onchange('qty')
    def _check_dispatch_qty(self):
        for record in self:
            
            if record.qty > record.sales_order_.mfgqty or record.sales_order_.bal_to_disp < 0:
                raise exceptions.ValidationError("Dispatch quantity cannot be greater than the quantity in the sales order or the balance to dispatch is less than 0.")

    @api.onchange('item_')
    def onchange_item(self):
        if self.item_:
            sale_orders = self.env['sales_order_system.sales_order'].search([('so_code', '=', self.sales_order_.so_code)])
            if sale_orders:
                self.sales_order_ = sale_orders[0]

# transion model disp
class Tdisp(models.TransientModel):
    _name = 'sales_order_system.tdisp'
    
    dispatch_date = fields.Date(string='Dispatch Date', default=lambda self: fields.Date.today())  
    sales_order_ = fields.Many2one('sales_order_system.sales_order', string='Sales Order')
    customer_master_ = fields.Many2one(related='sales_order_.cutomer_', string='Customer Name')
    item_ = fields.Many2one(related='sales_order_.item_rate_.item_', string='Item Rate')
    qty = fields.Integer(string='Quantity')
    agree_rate = fields.Text(related='sales_order_.item_rate_.agree_rate', string='Rate')
    amount = fields.Float(string='Amount', compute="_compute_amount")
    
   
    
    
    def genbook(self):
        if self.qty > self.sales_order_.mfgqty or self.sales_order_.bal_to_disp < 0:
                raise UserError("Dispatch quantity cannot be greater than the quantity in the sales order or the balance to dispatch is less than 0.")


        if  self.sales_order_.bal_to_disp <= 0:
            self.sales_order_.state = 'closed'
            
        bo = self.env[ 'sales_order_system.dispatch' ].create( {
                                    'dispatch_date': self.dispatch_date,
                                    'sales_order_': self.sales_order_.id,
                                    'customer_master_': self.customer_master_,
                                    'item_': self.item_,
                                    'qty': self.qty,
                                    'agree_rate': self.agree_rate,
                                    'amount': self.amount,
                                    
                                    } )
        return True
        # dis = {
        #     'type': 'ir.actions.act_window',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'sales_order_system.dispatch',
        #     'res_id': bo.id,
        #     }
        
        

    @api.depends('qty')
    def _compute_amount(self):
        logger = logging.getLogger(__name__)

        for dispatch_record in self:
            try:
                agree_rate = float(dispatch_record.agree_rate or 0)
                amount = dispatch_record.qty * agree_rate
                dispatch_record.amount = amount
                logger.info(f"Computed amount for Dispatch {dispatch_record.id}: {amount}")
            except ValueError:
                logger.error(f"Invalid agree_rate value for Dispatch {dispatch_record.id}: {dispatch_record.agree_rate}")

        return True
                
    # @api.onchange('qty')
    # def _check_dispatch_qty(self):
    #     for record in self:
            
    #         if record.qty > record.sales_order_.mfgqty or record.sales_order_.bal_to_disp < 0:
    #             raise exceptions.ValidationError("Dispatch quantity cannot be greater than the quantity in the sales order or the balance to dispatch is less than 0.")


    # @api.onchange('item_')
    # def onchange_item(self):
    #         if self.item_:
    #             sale_orders = self.env['sales_order_system.sales_order'].search([('so_code', '=', self.sales_order_.so_code)])
    #             if sale_orders:
    #                 self.sales_order_ = sale_orders[0]