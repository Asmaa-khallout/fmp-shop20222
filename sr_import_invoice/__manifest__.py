# -*- coding: utf-8 -*-
{
    'name': "Import Customer Invoices/Vendor Bills/ Customers  Refunds/ Vendors Refunds",
    'summary': "This module helps you to import Customer Invoices/Vendor Bills/ Customers  Refunds/ Vendors Refunds",
    'category': 'Accounting',
    'description': """
        Using this module Customer Invoices/Vendor Bills/ Customers  refunds/ Vendors Refunds is imported using excel sheets
    import customers Invoice using csv 
    import customers Invoice using xls
    import customers Refund using csv 
    import customers Refund using xls
    import Vendors Bills using csv 
    import Vendors Bills using xls
    import Vendors Refund using csv 
    import Vendors Refund using xls
    import with invoice state configuration
    import draft invoice
    import open invoice
    update invoice
    import with custom sequence
    import with default sequence
    import with product name/code/barcode
    import with customers/vendors name or reference code
    import custom account in invoice line
    """,
    'images': ['static/description/banner.png'],
    "price": 20,
    "currency": 'EUR',

    'depends': ['base',
                'sale_management'],

    'data': [
        'wizard/sr_import_invoice.xml',

    ],
}
