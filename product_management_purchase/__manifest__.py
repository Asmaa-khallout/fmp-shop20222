# -*- coding: utf-8 -*-
{
    "name": "Product Management Interface: Purchases",
    "version": "15.0.1.0.1",
    "category": "Purchases",
    "author": "faOtools",
    "website": "https://faotools.com/apps/15.0/product-management-interface-purchases-601",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "product_management",
        "purchase"
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/add_prm_vendor.xml",
        "wizard/update_purchase_policy.xml",
        "wizard/update_prm_pricedifferenceaccount.xml",
        "views/product_template.xml",
        "data/data.xml"
    ],
    "assets": {},
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The extension for the tool Product Management Interface to add purchasing mass actions",
    "description": """
For the full details look at static/description/index.html

* Features * 




#odootools_proprietary

    """,
    "images": [
        "static/description/main.png"
    ],
    "price": "10.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=89&ticket_version=15.0&url_type_id=3",
}