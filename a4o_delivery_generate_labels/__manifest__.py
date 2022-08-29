# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
{
    'name': 'Module Delivery Generate Labels',
    'version': '15.0.2',
    'author': 'Adiczion SARL',
    'category': 'Adiczion',
    'license': 'AGPL-3',
    'depends': [
        'delivery',
    ],
    'demo': [],
    'website': 'http://adiczion.com',
    'description': """
Module Delivery Generate Labels
===============================

Module used to generate labels, corresponding to the chosen carrier, from
a selection of packages to be shipped.

Also allows you to generate labels on demand.

The option: Default weight of the package, in the warehouse configuration,
allows you to request the label even if the weights are not entered in the
products.

    """,
    'data': [
        # 'security/objects_security.xml',
        'security/ir.model.access.csv',
        # 'wizard/your_wizard_name.xml',
        # 'data/data_for_your_module.xml',
        'views/stock_warehouse_views.xml',
        'views/res_config_views.xml',
        'views/generate_label_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'test': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
