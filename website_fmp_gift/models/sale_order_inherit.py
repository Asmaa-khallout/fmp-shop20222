# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.tools.misc import formatLang
import logging

_logger = logging.getLogger(__name__)

class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    def _pay_with_gift_card(self, gift_card):
        error = False

        if not gift_card.can_be_used():
            error = _('Invalid or Expired Gift Card.')
        elif gift_card in self.order_line.mapped("gift_card_id"):
            error = _('Gift Card already used.')
        elif gift_card.partner_id and gift_card.partner_id != self.env.user.partner_id:
            error = _('Gift Card are restricted for another user.')

        amount = min(self.amount_untaxed, gift_card.balance_converted(self.currency_id))
        if not error and amount > 0:
            pay_gift_card_id = self.env.ref('gift_card.pay_with_gift_card_product')
            gift_card.redeem_line_ids.filtered(lambda redeem: redeem.state != "sale").unlink()
            self.env["sale.order.line"].create({
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

    def _get_reward_values_discount_fixed_amount(self, program):
        total_amount = sum(self._get_base_order_lines(program).mapped('price_subtotal'))
        fixed_amount = program._compute_program_amount('discount_fixed_amount', self.currency_id)
        _logger.info("les totauuuuuux %s" %(total_amount,fixed_amount))
        if total_amount < fixed_amount:
            return total_amount
        else:
            return fixed_amount



    def _get_reward_values_percentage_amount(self, program):
        _logger.info("iciiii asmaa percentage!!!")
        # Invalidate multiline fixed_price discount line as they should apply after % discount
        fixed_price_products = self._get_applied_programs().filtered(
            lambda p: p.discount_type == 'fixed_amount'
        ).mapped('discount_line_product_id')
        self.order_line.filtered(lambda l: l.product_id in fixed_price_products).write({'price_unit': 0})

        reward_dict = {}
        lines = self._get_paid_order_lines()
        amount_total = sum([line.price_subtotal
                            for line in self._get_base_order_lines(program)])
        _logger.info("amount total %s" %(amount_total))
        if program.discount_apply_on == 'cheapest_product':
            line = self._get_cheapest_line()
            if line:
                discount_line_amount = min(line.price_reduce * (program.discount_percentage / 100), amount_total)
                _logger.info("price percentage %s et amout tota %s" %(discount_line_amount,amount_total))
                if discount_line_amount:
                    taxes = self.fiscal_position_id.map_tax(line.tax_id)

                    reward_dict[line.tax_id] = {
                        'name': _("Discount: %s", program.name),
                        'product_id': program.discount_line_product_id.id,
                        'price_unit': - discount_line_amount if discount_line_amount > 0 else 0,
                        'product_uom_qty': 1.0,
                        'product_uom': program.discount_line_product_id.uom_id.id,
                        'is_reward_line': True,
                        'tax_id': [(4, tax.id, False) for tax in taxes],
                    }
        elif program.discount_apply_on in ['specific_products', 'on_order']:
            if program.discount_apply_on == 'specific_products':
                # We should not exclude reward line that offer this product since we need to offer only the discount on the real paid product (regular product - free product)
                free_product_lines = self.env['coupon.program'].search([('reward_type', '=', 'product'), ('reward_product_id', 'in', program.discount_specific_product_ids.ids)]).mapped('discount_line_product_id')
                lines = lines.filtered(lambda x: x.product_id in (program.discount_specific_product_ids | free_product_lines))

            # when processing lines we should not discount more than the order remaining total
            currently_discounted_amount = 0
            _logger.info("eliiif")
            for line in lines:
                discount_line_amount = min(self._get_reward_values_discount_percentage_per_line(program, line), amount_total - currently_discounted_amount)
                _logger.info("discount line amount :%s" %(discount_line_amount))
                if discount_line_amount:

                    if line.tax_id in reward_dict:
                        reward_dict[line.tax_id]['price_unit'] -= discount_line_amount
                    else:
                        taxes = self.fiscal_position_id.map_tax(line.tax_id)

                        reward_dict[line.tax_id] = {
                            'name': _(
                                "Discount: %(program)s - On product with following taxes: %(taxes)s",
                                program=program.name,
                                taxes=", ".join(taxes.mapped('name')),
                            ),
                            'product_id': program.discount_line_product_id.id,
                            'price_unit': - discount_line_amount if discount_line_amount > 0 else 0,
                            'product_uom_qty': 1.0,
                            'product_uom': program.discount_line_product_id.uom_id.id,
                            'is_reward_line': True,
                            'tax_id': [(4, tax.id, False) for tax in taxes],
                        }
                        currently_discounted_amount += discount_line_amount

        # If there is a max amount for discount, we might have to limit some discount lines or completely remove some lines
        max_amount = program._compute_program_amount('discount_max_amount', self.currency_id)
        if max_amount > 0:
            amount_already_given = 0
            for val in list(reward_dict):
                amount_to_discount = amount_already_given + reward_dict[val]["price_unit"]
                if abs(amount_to_discount) > max_amount:
                    reward_dict[val]["price_unit"] = - (max_amount - abs(amount_already_given))
                    add_name = formatLang(self.env, max_amount, currency_obj=self.currency_id)
                    reward_dict[val]["name"] += "( " + _("limited to ") + add_name + ")"
                amount_already_given += reward_dict[val]["price_unit"]
                if reward_dict[val]["price_unit"] == 0:
                    del reward_dict[val]
        return reward_dict.values()


    # def _get_reward_values_discount_percentage_per_line(self, program, line):
    #     #discount_amount= self.amount_untaxed * (program.discount_percentage / 100)
    #
    #     discount_amount = line.product_uom_qty * line.price_reduce * (program.discount_percentage / 100)
    #     #_logger.info("totaaal d order %s" %(self.amount_untaxed))
    #     #_logger.info("line price reduce %s  ,, %s " % (line.price_reduce, program.discount_percentage))
    #     _logger.info(discount_amount)
    #     return discount_amount
