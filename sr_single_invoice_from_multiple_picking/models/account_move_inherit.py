from odoo import models, fields


class account_move(models.Model):
    _inherit = 'account.move'

    custom_picking_ids = fields.Many2many('stock.picking', string="Pickings")

    def check_payment(self):
        for payment in self.env['account.payment'].search([]):
            if self.id in payment.reconciled_invoice_ids.ids:
                return payment

    def _find_picking_details(self):
        final_list = []
        for picking in self.custom_picking_ids:
            amount_total = 0
            invoice_line_search = self.env['account.move.line'].search([('custom_move_id.picking_id', '=', picking.id)])
            for new_line in invoice_line_search:
                amount_total += new_line.price_subtotal
            final_list.append({
                'picking': picking.name,
                'date': picking.scheduled_date,
                'ref': picking.group_id.sale_id.client_order_ref,
                'amount': amount_total
            })
        print("=======final_list===", final_list)
        return final_list

    def _find_move_details(self, pick):
        invoice_line_search = self.env['account.move.line'].search([('custom_move_id.picking_id', '=', pick.id)])
        return invoice_line_search

    def button_cancel(self):
        res = super(account_move, self).button_cancel()
        if self.custom_picking_ids:
            for pick in self.custom_picking_ids:
                pick.is_invoiced = False
        return res


class account_move_line(models.Model):
    _inherit = 'account.move.line'

    custom_move_id = fields.Many2one('stock.move', string="Move")

    def _get_customer_product_code(self):
        customer_ids = self.env['product.customer.info'].search(
            [('product_id', '=', self.product_id.id), ('partner_id', '=', self.partner_id.id)])
        if customer_ids:
            return customer_ids[0].customer_product_code
        else:
            return '-'

    def _get_customer_product_name(self):
        customer_ids = self.env['product.customer.info'].search(
            [('product_id', '=', self.product_id.id), ('partner_id', '=', self.partner_id.id)])
        if customer_ids:
            return customer_ids[0].customer_product_name
        else:
            return '-'
