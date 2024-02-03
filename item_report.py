import odoo.tools as tools
import datetime, calendar
from odoo import api, fields, models
import logging
import json
_logger = logging.getLogger(__name__)
from dateutil.rrule import rrule, DAILY
import time


class ItemReport(models.TransientModel):
    _name = 'sales_order_system.reportx1'
    _inherit = 'report.report_xlsx.abstract'
    
    mon = fields.Char( 'Selected Month', size = 20, compute='_mon' )
    mondate = fields.Date( 'Select Date', default=lambda self: fields.Date.today() )  
    custlist = fields.Boolean( 'List of customer', default=True, readonly = True )
   
   
    @api.depends( 'mondate' )
    def _mon( self ):
        for o in self:
            o.mon = o.mondate.strftime( '%b %Y' )
            mon = o.mondate.month         
           
           
    def generate( self ):
        data = {}
        return self.env.ref('sales_order_system.sales_order_system_reportx1').sudo().report_action(self, data)
    
    
    def getreportpath( self ):
        return self.env['ir.config_parameter'].sudo().get_param('reportpath') or tools.config['addons_path']


    def generate_xlsx_report(self, workbook, data, o):
        _logger.info( "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< " + tools.config['addons_path'] )
        rpath = self.getreportpath( )
        rname = 'PR'

        rdict = o.reportcalc()
        _logger.info( rdict )

        with open( rpath + '/sales_order_system/rx1.format.py', 'r') as file:
            exec( file.read() )        
        if o.custlist:
            rname = rname + '_PR'
            with open( rpath + '/sales_order_system/rx1.custlist.py', 'r') as file:
                exec( file.read() )
        
        rname = rname + '_' + o.mon
            
        r = self.env['ir.actions.report'].sudo().search( [ ( 'report_name','=',o._name ) ] )[0]
        r.sudo().report_file = rname
    
    
    
    def reportcalc(self):
        r = {}
        c = self.env['sales_order_system.trans1'].search([])

        for record in c:
            item_name = record.item_.item_name
            total_mfg_qty = record.total_mfg_qty
            total_disp_qty = record.total_disp_qty
            open_order_qty = record.open_order_qty

            # Assuming item_name is unique, you can use it as the key in the dictionary
            r[item_name] = {
                'total_mfg_qty': total_mfg_qty,
                'total_disp_qty': total_disp_qty,
                'open_order_qty': open_order_qty,
            }

        _logger.info(r)
        return r
    
    
    
        # def reportcalc(self):
        #     o = self
        #     rdict = {}
        #     c = self.env['sales_order_system.trans1'].search([])
        #     _logger.info(c)
        #     for i in c:
        #         cid = i.ref
        #         # Add other fields to the dictionary
        #         other_fields = {
        #             'item_': i.item_.id if i.item_ else None,
        #             'total_mfg_qty': i.total_mfg_qty,
        #             'total_disp_qty': i.total_disp_qty,
        #             'open_order_qty': i.open_order_qty,
        #         }
        #         rdict[cid] = other_fields

        #     return rdict
            
 
		