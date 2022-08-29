# -*- coding: utf-8 -*-
{
    'name': "Product Customer Code",
    'summary': "Allows to manage customer specific product code and product name",

    'description': """
            This module will introduce a new feature to manage customer specific product code and product name. those product code and product name will be displayed in description(name) field of product lines.
            This description(name) field is display on reports(quotation and invoice).
        """,
    'category': 'Sales',
    'version': '0.1',

    'depends': ['base',
                'sale_management'
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],

}
