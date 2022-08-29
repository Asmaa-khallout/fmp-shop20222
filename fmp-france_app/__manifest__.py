# -*- coding: utf-8 -*-
{
    'name': "FMP FRANCE app",
    'summary': """ fmp_france.mg """,
    'static': """ fmp_france.mg """,
    'author': "KASIA SARL",
    'website': "https://kasia.mg",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'fmp-france_base',
        'fmp-contact_activation',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
    ],
}
