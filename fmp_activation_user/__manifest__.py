# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'FMP Activation User',
    'version' : "15.0.0.0",
    'description' : """
        
        

     """,
    'author' : "Asmaa Khallout",
    'website'  : "https://dkgroup.fr",
    'depends': ['base','auth_signup','crm'],
    'data'     : ['views/auth_signup_inherit_views.xml',
                  'views/res_partner_inherit_views.xml',
                  'data/mail_template.xml',
                  'views/activation_template.xml',
                  ],
    'installable' : True,
    'application' :  True,
}
