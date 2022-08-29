# -*- coding: utf-8 -*-
{
    'name': 'Import Vendor Details in Product odoo',
    'version': '13.0.0.0',
    'sequence': 4,
    'summary': 'This apps helps to import product with supplier details',
    'description': """
    """,
    'price': 20.00,
    'currency': "EUR",

    'depends': ['base',
                'sale_management',
                'purchase',
                'stock'],

    'data': ["supp_info.xml"
            ],
}
