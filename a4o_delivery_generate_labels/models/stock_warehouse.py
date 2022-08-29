# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from odoo import fields, models


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    default_package_weight = fields.Float(string='Default Package Weight',
        default=0.1,
        help="Default weight limit for the grouped generation of labels "
             "before packaging.")
