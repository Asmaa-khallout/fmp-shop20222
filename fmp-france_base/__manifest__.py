# -*- coding: utf-8 -*-
{
    'name': "FMP FRANCE Base",
    'summary': """ fmp_france.mg """,
    'static': """ fmp_france.mg """,
    'author': "KASIA SARL",
    'website': "https://kasia.mg",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'contacts',
        'crm',
        'purchase',
        'sale',
        'stock',
        'website_sale',
        'customer_sale_history',
        'customer_sequence',
        'product_customer_info',
        'sales_margin_percentage',
        'sr_import_invoice',
        'sr_import_product_customer_info',
        'sr_import_purchase_order_lines',
        'sr_import_sales_order_line',
        'sr_import_supplier_info',
        'a4o_delivery_chronopost',
        'a4o_delivery_generate_labels',
        'a4o_delivery_relaypoint',
        'payment_lyra',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
    ],
}
