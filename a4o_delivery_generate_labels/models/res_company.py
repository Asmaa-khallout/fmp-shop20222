# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from odoo import fields, models, _


class Company(models.Model):
    _inherit = "res.company"

    all_attachments_on_pdf = fields.Boolean('All attachments of picking(s)',
        help="Take all the attachments for generate one pdf on selected "
             "picking(s)")
