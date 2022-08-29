# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    numero_siret = fields.Char("Siret",related="partner_id.numero_siret")
    name_shop = fields.Char('Name of shop',related="partner_id.name_shop")
