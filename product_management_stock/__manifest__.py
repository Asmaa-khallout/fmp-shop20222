# -*- coding: utf-8 -*-
{
    "name": "Product Management Interface: Warehouse",
    "version": "15.0.1.0.1",
    "category": "Warehouse",
    "author": "faOtools",
    "website": "https://faotools.com/apps/15.0/product-management-interface-warehouse-602",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "product_management",
        "stock"
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/update_prm_production_location.xml",
        "wizard/update_prm_inventory_location.xml",
        "wizard/update_prm_routes.xml",
        "wizard/update_prm_tracking.xml",
        "views/product_template.xml",
        "data/data.xml"
    ],
    "assets": {},
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The extension for the tool Product Management Interface to add WMS mass actions",
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
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=90&ticket_version=15.0&url_type_id=3",
}