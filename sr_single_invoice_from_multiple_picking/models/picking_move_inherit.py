from odoo import models, fields


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def create_invoices(self):
        res = super(SaleAdvancePaymentInv, self).create_invoices()
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        for orders in sale_orders:
            for pick in orders.picking_ids:
                pick.is_invoiced = True
        return res


class StockPikcing(models.Model):
    _inherit = 'stock.picking'

    is_invoiced = fields.Boolean(string="Invoiced")
    invoice_count = fields.Float(compute="_compute_invoice", string="Invoice", copy=False, default=0)

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id,
                               values):
        move_values = super(StockRule, self)._get_stock_move_values(self, product_id, product_qty, product_uom,location_id, name, origin, company_id, values)
        move_values.update({'created_sale_order_line_id': values.get('sale_line_id'), })
        return move_values

    def _compute_invoice(self):
        for order in self:
            if order.sale_id:
                invoices = order.sale_id.order_line.invoice_lines.move_id
                self.invoice_count = len(invoices)
            elif order.purchase_id:
                order.purchase_id.sudo()._read(['invoice_ids'])
                self.invoice_count = len(order.purchase_id.invoice_ids)
            else:
                invoice = self.env['account.move'].search([('custom_picking_ids', 'in', order.id)])
                self.invoice_count = len(invoice)

    def action_view_invoice(self):
        if self.picking_type_id.code == 'incoming':
            action = self.env.ref('account.action_move_in_invoice_type')
            invoice = self.purchase_id.invoice_ids
        else:
            action = self.env.ref('account.action_move_out_invoice_type')
            invoice = self.sale_id.order_line.invoice_lines.move_id
        result = action.read()[0]
        print("=========inv", invoice)
        result['domain'] = "[('id', 'in', " + str([a.id for a in invoice]) + ")]"
        return result
