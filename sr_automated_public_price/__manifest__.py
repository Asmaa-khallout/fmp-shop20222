# -*- coding: utf-8 -*-
{
    'name': 'Automatec Public Price',
    'summary': 'This module will help you to set automatic public price',
    'category': 'Sales',

    'depends': ['base',
                'sale',
                'product',
                # 'sr_manual_currency_exchange_rate'
                ],

    'data': [
        # 'data/ir_cron.xml',
        'security/ir.model.access.csv',
        'sr_automated_price_view.xml',
    ],
}
