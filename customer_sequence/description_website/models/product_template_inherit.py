# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.tools.translate import html_translate


class ProductTemplateInherit(models.Model):

    _inherit = "product.template"

    website_short_description = fields.Html("Short description for the website", sanitize_attributes=False, translate=html_translate)