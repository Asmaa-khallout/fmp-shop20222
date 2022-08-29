#  -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime
import ast
import logging

_logger = logging.getLogger(__name__)


class CouponProgramInherit(models.Model):
    _inherit = 'coupon.program'

    def _check_promo_code_portal(self, order, coupon_code):
        message = {}
        if self.maximum_use_number != 0 and self.total_order_count >= self.maximum_use_number:
            message = {'error': _('Promo code %s has been expired.') % (coupon_code)}
        elif not self.active:
            message = {'error': _('Promo code is invalid')}
        elif self.rule_date_from and self.rule_date_from > fields.Datetime.now():
            tzinfo = self.env.context.get('tz') or self.env.user.tz or 'UTC'
            locale = self.env.context.get('lang') or self.env.user.lang or 'en_US'
            message = {'error': _('This coupon is not yet usable. It will be starting from %s') % (format_datetime(self.rule_date_from, format='short', tzinfo=tzinfo, locale=locale))}
        elif self.rule_date_to and fields.Datetime.now() > self.rule_date_to:
            message = {'error': _('Promo code is expired')}
        return message

