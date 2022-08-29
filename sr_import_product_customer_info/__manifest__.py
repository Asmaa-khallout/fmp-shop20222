# -*- coding: utf-8 -*-
{
    'name': "Import Product Customer Information",
    'category': 'Sales',
    'version': '0.1',

    'depends': ['base',
                'sale',
                'product_customer_info'],

    'data': [
        'wizards/sr_import_attendance_wizard.xml',
        'views/sr_import_menu_views.xml',
    ],
    "price": 0,
    "currency": 'EUR',
}
