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
    ],
    'data' : [
        'security/ir.model.access.csv',
        'views/res_company_views.xml',
        'views/sale_view.xml',
        'views/menu.xml',
        'report/conditions_generales_de_vente_templates.xml',
        'report/report_invoice.xml',
        'report/sale_report_templates.xml',
        'report/report_templates.xml',




    ],
    'installable': True,
    'application': True,
    'qweb': [
    ],
}

