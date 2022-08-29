# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = 'product.template'

    rack_number = fields.Char("Rack Number")


class StockMove(models.Model):
    _inherit = 'stock.move'

    rack_number = fields.Char(related='product_id.rack_number', string="Rack Number")
