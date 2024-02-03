import datetime
from odoo import api, fields, models, exceptions

# class department():
    # descrip....
    # editable tree view

class Customer_master(models.Model):
    _name = 'sales_order_system.customer_master'
    _description = 'customer_master'

    customer_code = fields.Text('Customer_code', default='new', readonly=True)
    customer_name = fields.Text('Customer_name', required = True)
    image = fields.Binary('Image')
    files = fields.Binary('Files')
    
    _rec_name = "customer_name"

    
    @api.model
    def create(self, vals):
        vals['customer_code']=self.env['ir.sequence'].next_by_code('sales_order_system.customer_master')
        ite = super().create(vals)
        return ite
    


    


# how to remove create new
# disable item rate field if no customer
# show rate on change of item rate
# stored computed field??
# how to save time in closing and restarting odoo server
# default to today's date?

    
    
   