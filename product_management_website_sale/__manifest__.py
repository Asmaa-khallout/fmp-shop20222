# -*- coding: utf-8 -*-
{
    "name": "Product Management Interface: e-Commerce",
    "version": "15.0.1.0.1",
    "category": "Sales",
    "author": "faOtools",
    "website": "https://faotools.com/apps/15.0/product-management-interface-e-commerce-600",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "product_management",
        "website_sale"
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/update_prm_public_categories.xml",
        "wizard/update_prm_alternatives.xml",
        "wizard/update_prm_accessories.xml",
        "views/product_template.xml",
        "data/data.xml"
    ],
    "assets": {},
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The extension for the tool Product Management Interface to add e-shop mass actions",
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
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=88&ticket_version=15.0&url_type_id=3",
}