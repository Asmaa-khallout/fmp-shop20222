# -*- coding: utf-8 -*-
{
    'name': 'Add rack number in products',
    'version': '0.1',
    'category': 'Products',
    'summary': 'This module allows you to add rack number in product.',
    'description': """
            This module allows you to add rack number in product.
    """,
    "price": 000,
    "currency": 'EUR',

    'depends': ['base',
                'product',
                'stock'],

    'data': [
        'views/product_inherit.xml',
    ],
}
