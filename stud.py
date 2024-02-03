import datetime
from odoo import api, fields, models, exceptions

# class department():
    # descrip....
    # editable tree view

class Student(models.Model):
    _name = 'sales_order_system.student'
    _description = 'student info'

    name = fields.Text('Student', required = True)
    auto = fields.Text('Autocode', default='new', readonly=True)
    gender = fields.Selection([('F', 'Female'), ('M', 'Male')],' gender ', required = True)
    bod = fields.Date('Birth date ', required = True)
    add = fields.Char('Address', size=50)
    hobby = fields.Text('Hobby')
    mark = fields.Integer('Mark')
    
    @api.model
    def create(self, vals):
        vals['auto']=self.env['ir.sequence'].next_by_code('sales_order_system.student')
        o = super().create(vals)
        return o



    
    
   