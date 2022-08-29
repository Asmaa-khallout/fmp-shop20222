# -*- coding: utf-8 -*-
{
    'name': "Create Single Invoice From Multiple Picking",
    'summary': "This module allows you to create single invoice from multiple picking",
    'category': 'Invoicing Management',
    'description': """
    Create single invoice from multiple pickings
    Create single customer invoice from multiple delivery picking
    Create single vendor invoice from multiple incoming picking
    Create single vendor invoice from purchase picking
    Create single customer invoice from outgoing delivery picking
    Generate single invoice from pickings
    Generate single customer invoice from delivery orders
    Generate single customer invoice from outgoing picking
    Generate single vendor invoice from incoming picking
    generate single customer invoice
    generate single vendor bill
    generate single supplier invoice
    generate single vendor invoice
    multiple picking generate single invoice

    """,
    'depends': ['base',
                'account',
                'sale_management',
                'stock',
                'purchase'],
    'data': [
        'wizard/generate_single_invoice.xml',
        'reports/account_report_picking.xml',
        'reports/report_invoice_picking.xml',
        'reports/inherit_invoice_order_report.xml',
        'reports/inherit_picking_slip_report.xml'

    ],
    'images': ['static/description/banner.png'],
    "price": 15,
    "currency": 'EUR',
}
