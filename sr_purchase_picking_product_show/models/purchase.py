from odoo import api, fields, models
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    product_count = fields.Float(compute="_compute_product", string="Product", copy=False, default=0, store=True)

    @api.depends('order_line.product_id')
    def _compute_product(self):
        for order in self:
            products = order.mapped('order_line.product_id')
            order.product_count = len(products)

    def action_view_product(self):
        action = self.env.ref('stock.stock_product_normal_action')
        result = action.read()[0]
        result['domain'] = "[('id', 'in', " + str([a.product_id.id for a in self.order_line]) + ")]"
        return result
