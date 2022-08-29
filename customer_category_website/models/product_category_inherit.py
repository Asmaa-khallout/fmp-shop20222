# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductCategoryInherit(models.Model):
    _inherit = "product.public.category"

    active = fields.Boolean('Actif',default=True)

