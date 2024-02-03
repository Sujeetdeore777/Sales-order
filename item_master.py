import datetime
from odoo import api, fields, models, exceptions

# class department():
    # descrip....
    # editable tree view

class Item_master(models.Model):
    _name = 'sales_order_system.item_master'
    _description = 'item_master'

    item_code = fields.Text('Item_code', default='new', readonly=True)
    item_name = fields.Text('Item_name', required = True)
    part_no = fields.Char('Part_no', size=50)
    
    _rec_name = "item_name"
    
    @api.model
    def create(self, vals):
        vals['item_code'] = 'S-' + self.env['ir.sequence'].next_by_code('sales_order_system.item_master')
        ite = super().create(vals)
        return ite

    




    
    
   