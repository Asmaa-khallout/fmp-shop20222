#  -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class GiftCardInherit(models.Model):
    _inherit = 'gift.card'

    libelle = fields.Char("Libelle")
    note = fields.Text("Note")