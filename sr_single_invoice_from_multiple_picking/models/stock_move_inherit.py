from odoo import models, fields


class stock_move(models.Model):
    _inherit = 'stock.move'

    created_sale_order_line_id = fields.Many2one('sale.order.line', string="Order Line")
