# -*- coding: utf-8 -*-

from odoo import models, fields


class CompanySequence(models.Model):
    _inherit = 'res.company'

    customer_code = fields.Integer(string='Customer code', required=True)
    next_code = fields.Integer(string='Next code')
