# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
import logging

_logger = logging.getLogger(__name__)

class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    def _pay_with_gift_card(self, gift_card):
        _logger.info("asmaaaaaaaaaa la pay with gift")
        _logger.info(self.amount_untaxed)
        error = False

        if not gift_card.can_be_used():
            error = _('Invalid or Expired Gift Card.')
        elif gift_card in self.order_line.mapped("gift_card_id"):
            error = _('Gift Card already used.')
        elif gift_card.partner_id and gift_card.partner_id != self.env.user.partner_id:
            error = _('Gift Card are restricted for another user.')

        amount = min(self.amount_untaxed, gift_card.balance_converted(self.currency_id))
        _logger.info(amount)
        if not error and amount > 0:
            pay_gift_card_id = self.env.ref('gift_card.pay_with_gift_card_product')
            gift_card.redeem_line_ids.filtered(lambda redeem: redeem.state != "sale").unlink()
            line= self.env["sale.order.line"].create({
                'product_id': pay_gift_card_id.id,
                'price_unit': -amount,
                'product_uom_qty': 1,
                'product_uom': pay_gift_card_id.uom_id.id,
                'gift_card_id': gift_card.id,
                'order_id': self.id
            })
        return error

    def _recompute_gift_card_lines(self):
        for record in self:
            lines_to_remove = self.env['sale.order.line']
            lines_to_update = []

            gift_payment_lines = record.order_line.filtered('gift_card_id')
            to_pay = sum((self.order_line - gift_payment_lines).mapped('price_subtotal'))

            # consume older gift card first
            for gift_card_line in gift_payment_lines.sorted(lambda line: line.gift_card_id.expired_date):
                amount = min(to_pay, gift_card_line.gift_card_id.balance_converted(record.currency_id))
                if amount:
                    to_pay -= amount
                    if gift_card_line.price_unit != -amount or gift_card_line.product_uom_qty != 1:
                        lines_to_update.append(
                            fields.Command.update(gift_card_line.id, {'price_unit': -amount, 'product_uom_qty': 1})
                        )
                else:
                    lines_to_remove += gift_card_line
            lines_to_remove.unlink()
            record.update({'order_line': lines_to_update})