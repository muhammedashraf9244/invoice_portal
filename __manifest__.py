# -*- coding: utf-8 -*-
{
    'name': "invoice_portal",

    'summary': """
       """,

    'description': """
       
    """,

    'author': "HAFSSA AZIM",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account', 'portal'],

    # always loaded
    'data': [
        'views/templates.xml',
        'views/asset.xml',
        'views/report_invoice_template.xml',
        'views/invoice_portal_report.xml',
        'data/cron_job.xml',
    ],

}
