# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    all_attachments_on_pdf = fields.Boolean(readonly=False,
        related='company_id.all_attachments_on_pdf',
        string="Take all attachments of picking(s)",
        help="Take all the attachments for generate one pdf on selected "
             "picking(s)")
