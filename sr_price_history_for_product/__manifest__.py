# -*- coding: utf-8 -*-
{
    'name': "Sales and Purchase Price History for Products",
    'summary': "With the help of this module, You can find the rate which you have given to that customers/suppliers in past for that product.",
    'category': 'Sales',
    'description': """
    purchase price history
    sale price history
    easy to find previous cost price
    easy to find previous sale price
    price history
    purchase cost history
    inherit product
    track the price in product template
    track the price in product variant
    product wise sale price history
    product wise purchase price history
    product wise sale history

    """,
    'depends': ['base',
                'sale_management',
                'purchase'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_inherit.xml',
        'views/res_config_sett_inherit.xml',
    ],
    'live_test_url': 'https://youtu.be/VGs7aaPtW9s',
    'images': ['static/description/banner.png'],
    "price": 0,
    "currency": 'EUR',
}
