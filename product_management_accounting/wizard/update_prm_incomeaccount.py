# -*- coding: utf-8 -*-

from odoo import api, fields, models

class update_prm_incomeaccount(models.TransientModel):
    _name = "update.prm.incomeaccount"
    _inherit = "product.sample.wizard"
    _description = "Update income account"

    incomeaccount_id = fields.Many2one(
        "account.account",
        string="New income account",
        domain=[('deprecated', '=', False)],
        required=True,
    )

    def _update_products(self, product_ids):
        """
        The method to prepare new vals for income account

        Args:
         * product_ids - product.template recordset

        Extra info:
         * Expected singleton
        """
        self.ensure_one()
        product_ids.write({"property_account_income_id": self.incomeaccount_id.id})
