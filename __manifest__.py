# -*- coding: utf-8 -*-
{
    'name'     : 'InfoSaône - Module Odoo 12 pour Sintermat',
    'version'  : '0.1',
    'author'   : 'InfoSaône',
    'category' : 'InfoSaône',
    'description': """
InfoSaône - Module Odoo 12 pour Sintermat
===================================================
""",
    'maintainer' : 'InfoSaône',
    'website'    : 'http://www.infosaone.com',
    'depends'    : [
        'base',
        'document',
        'product',
        'sale',
        'purchase',
        'purchase_stock',
    ],
    'data' : [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/res_company_views.xml',
        'views/sale_view.xml',
        'views/stock_picking_views.xml',
        'views/menu.xml',
        'report/conditions_generales_de_vente_templates.xml',
        'report/report_invoice.xml',
        'report/sale_report_templates.xml',
        'report/purchase_order_templates.xml',
        'report/report_deliveryslip.xml',
        'report/report_templates.xml',
    ],
    'installable': True,
    'application': True,
    'qweb': [
    ],
}

