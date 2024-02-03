import datetime
from odoo import api, fields, models, exceptions
from odoo.exceptions import ValidationError

import base64
import datetime
# import pandas as pd
# from io import BytesIO

# class department():
    # descrip....
    # editable tree view

class trans(models.TransientModel):
    _name = 'sales_order_system.trans1'
    _description = 'trans'

    item_ = fields.Many2one('sales_order_system.item_master', string='Item', required=True)
    total_mfg_qty = fields.Float(string='Total Manufacturing Quantity', compute='compute_totals', store=False)
    total_disp_qty = fields.Float(string='Total Dispatch Quantity', compute='compute_totals', store=False)
    open_order_qty = fields.Float(string='Open Order Quantity', compute='compute_totals', store=False)
    

    @api.depends('item_')
    def compute_totals(self):
        for rec in self:
            item_id = rec.item_.id
            sales_orders = self.env['sales_order_system.sales_order'].search([('item_rate_.item_', '=', rec.item_.id), ('state','=','open')])
            rec.total_mfg_qty = sum(s.mfgqty for s in sales_orders)
            rec.total_disp_qty = sum(s.dispqty for s in sales_orders)
            rec.open_order_qty = sum(s.qty - s.mfgqty for s in sales_orders if s.state == 'open')
            
            
   