# -*- coding: utf-8 -*-
{
    'name': 'Delivery and Invoice Status in Sale Order',
    'summary': "Delivery and Invoice status in sales order.",
    'description': """
    Delivery and Invoice status in sales order
        """,
    'category': 'Sales',
    "license": "AGPL-3",
    'depends': ['sale_management',
                'stock',
                'account'],
    'data': [
        'views/sale_order.xml',
    ],
}
