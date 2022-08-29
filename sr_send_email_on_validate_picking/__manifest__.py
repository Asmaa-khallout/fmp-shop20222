# -*- coding: utf-8 -*-
{
    'name': 'Send email with excel and PDF attachments',
    'version': '0.1',
    'category': 'Inventory',
    'description': """
    """,
    "price": 000,
    "currency": 'EUR',
    'depends': ['base',
                'stock',
                'delivery'],

    'data': [
        # 'report/report_deliveryslip.xml',
        # 'report/stock_report_views.xml',
        # 'data/mail_template_data.xml',
        'data/ir_cron.xml',
        'views/partner_inherit.xml',
        'views/picking_inherit.xml'
    ],
}
