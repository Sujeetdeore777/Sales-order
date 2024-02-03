import datetime
from odoo import api, fields, models, exceptions

# class department():
    # descrip....
    # editable tree view

class Item_rate(models.Model):
    _name = 'sales_order_system.item_rate'
    _description = 'item_rate'

    item_ = fields.Many2one('sales_order_system.item_master', 'item_name')
    cutomer_ = fields.Many2one('sales_order_system.customer_master', 'customer_name')
    agree_rate = fields.Text('Agree_rate', required = True)
    
    _rec_name = "item_"


    
    
  

    




    
    
   