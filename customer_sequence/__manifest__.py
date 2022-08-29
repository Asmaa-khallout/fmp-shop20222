# -*- coding: utf-8 -*-
{
    'name': "Customer Sequence",
    'category': 'Sales',
    'version': '0.1',

    'depends': [
        'base',
        'sale',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_company.xml',
        'views/res_partner_form.xml',

    ],
    'images': ['static/description/banner.png'],
}
