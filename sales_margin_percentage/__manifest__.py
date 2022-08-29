# -*- coding: utf-8 -*-
{
    'name': "Sales Margin Percentage",
    'author': 'Ascetic Business Solution',
    'category': 'Sales',
    'summary': """Sales Margin Percentage in Quotation and Sales Order""",
    'license': 'AGPL-3',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'sale_management',
                'sale_margin'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
