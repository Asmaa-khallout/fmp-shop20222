# -*- coding: utf-8 -*-
{
    'name': "Test technical smile",
    'version': '0.1',

    'depends': [
        'base',
        'crm',
    ],

    'data': [
        'views/res_partner_inherit_views.xml',
        'views/crm_team_inherit_views.xml',
        #'views/crm_lead_inherit_views.xml',
        'data/ir_cron.xml',
    ]
}
