# -*- coding: utf-8 -*-
{
    'name': "FMP Contact activation",
    'summary': """
        Manage portal user activation process
        """,
    'description': """
        Manage portal user activation process
    """,
    'author': "KASIA SARL",
    'website': "https://kasia.mg",
    'category': 'Web',
    'version': '0.1',
    'depends': ['fmp-france_base','auth_signup','portal','website_sale'],
    'data': [
        # 'security/ir.model.access.csv',
        'data/mail_template.xml',
        'views/assets.xml',
        'views/partner_view.xml',
        'views/signup_templates.xml',
    ],
}
