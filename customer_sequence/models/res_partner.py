# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # unique_id = fields.Char(string='Unique Id', help="The Unique Sequence no", readonly=True, default='/')
    unique_id = fields.Char(string='Unique Id', help="The Unique Sequence no", readonly=False, default='/')

    # @api.model
    # def create(self, values):
    #     res = super(ResPartner, self).create(values)
    #     company_seq = self.env.company
    #     if res.customer_rank > 0 and res.unique_id == '/':
    #         if company_seq.next_code:
    #             res.unique_id = company_seq.next_code
    #             res.name = '[' + str(company_seq.next_code) + ']' + str(res.name)
    #             company_seq.write({'next_code': company_seq.next_code + 1})
    #         else:
    #             res.unique_id = company_seq.customer_code
    #             res.name = '[' + str(company_seq.customer_code) + ']' + str(res.name)
    #             company_seq.write({'next_code': company_seq.customer_code + 1})
    #     return res
