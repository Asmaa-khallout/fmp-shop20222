from odoo import models, fields

class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    parent_category_id =  fields.Many2many(related="parent_id.category_id",string="category parent")