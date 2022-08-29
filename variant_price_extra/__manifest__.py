# -*- coding: utf-8 -*-
{
    "name": "Product Variant Extra Price",
    "category": 'Uncategorized',
    "summary": """
            This module allows you to manually apply additional extra prices for Product's variants.""",
    "description": """
    ====================
    **Help and Support**
    ====================
    .. |icon_features| image:: variant_price_extra/static/src/img/icon-features.png
    .. |icon_support| image:: variant_price_extra/static/src/img/icon-support.png
    .. |icon_help| image:: variant_price_extra/static/src/img/icon-help.png

    |icon_help| `Help <http://webkul.uvdesk.com/en/customer/create-ticket/>`_ |icon_support| `Support <http://webkul.uvdesk.com/en/customer/create-ticket/>`_ |icon_features| `Request new Feature(s) <http://webkul.uvdesk.com/en/customer/create-ticket/>`_
        """,
    "sequence": 1,
    "version": '1.0',

    "depends": ['product'],

    "data": ['views/product_inherit_view.xml'],

    'images': ['static/description/Banner.png'],

    "price": 20,
    "currency": 'EUR',
}
