# -*- coding: utf-8 -*-

{
    'name': 'FMP France Custom Website',
    'category': 'Theme/eCommerce',
    'version': '15.0.0.2.2',
    'author': 'KHALLOUT Asmaa',
    'depends': ['theme_prime', 'website','description_website','fmp_activation_user','fmp_custom_portal'],
    'data': [
        #views
        'views/website_hompage_template.xml',
        #'views/website_header_template.xml',
        'views/website_footer_template.xml',
        'views/404_inherit_template.xml',
        'views/website_annex_template.xml',
        'views/website_product_template.xml',
        #'views/website_sale_products_template.xml',
        'views/website_payment_checkout_template.xml',
        'views/website_payment_checkout_template.xml',
        'views/website_cart_sidebar_template.xml',
        'views/website_login_template.xml',
        'views/website_confirmation_template.xml',
#        'views/website_contactus_template.xml',
        'views/website_search_template.xml',
        'views/option_back_to_top_template.xml',
        'views/website_cookies_bar_template.xml',
    ],
    "qweb": ["static/src/xml/website_sale_templates.xml"],
    "installable": True,
    "assets": {
        "web.assets_frontend": [
            "/fmp_france_custom_website/static/src/js/website_sale_hide_price.js"
        ]
    },
}
