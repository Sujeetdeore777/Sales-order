# -*- coding: utf-8 -*-

{
    'name': 'sales_order_system',
    'version': '1.1',
    'website': '',
    'category': 'MRP',
    'sequence': 10,
    'summary': 'sales order system',
    'depends': [
        'base','report_xlsx','web'
    ],
    'description': " sales order system",
    'data': [ 
              'security.xml',
              'ir.model.access.csv',
              'menu.xml',
              'stud.xml',
              'item_master.xml',
              'customer_master.xml',
              'item_rate.xml',
             'sales_order.xml',
              'dispatch.xml',
              'mfg.xml',
              'trans.xml',
              'report.xml',
              'item_report.xml',
             
    ],
    'qweb': [],
    
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
