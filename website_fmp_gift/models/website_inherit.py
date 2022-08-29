#  -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime
import ast
import logging
_logger = logging.getLogger(__name__)
class WebsiteInherit(models.Model):
	_inherit = 'website'

	def get_customer_gifts(self):
		order = self.sale_get_order()
		partner_id = self.env['res.users'].browse(self._uid).partner_id.id
		gift_ids = self.env['gift.card'].search([('expired_date','>=',fields.Date.today()),('partner_id','in',(False,partner_id)),('state','=','valid'),('balance','>', 0)])
		gifts = gift_ids.filtered(lambda r: r.can_be_used() and r not in order.order_line.mapped("gift_card_id"))
		return gifts

	def get_customer_coupon(self):
		coupon_ids =[]
		order = self.sale_get_order()
		programs = self.env['coupon.program'].search([('website_id', 'in', [False, self.id]),('active','=',True)])
		for program in programs:
			error_status = program._check_promo_code(order, program.promo_code)
			if error_status.get('error') or (program.program_type=='coupon_program' and program.coupon_count<1):
				continue
			coupon_ids += program
		return coupon_ids if len(coupon_ids)>0 else False