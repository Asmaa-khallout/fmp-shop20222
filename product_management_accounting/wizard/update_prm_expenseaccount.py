# -*- coding: utf-8 -*-

from odoo import api, fields, models

class update_prm_expenseaccount(models.TransientModel):
    _name = "update.prm.expenseaccount"
    _inherit = "product.sample.wizard"
    _description = "Update expense account"

    expenseaccount_id = fields.Many2one(
        "account.account",
        string="New expense account",
        domain=[('deprecated', '=', False)],
        required=True,
    )

    def _update_products(self, product_ids):
        """
        The method to prepare new vals for expense account

        Args:
         * product_ids - product.template recordset

        Extra info:
         * Expected singleton
        """
        self.ensure_one()
        product_ids.write({"property_account_expense_id": self.expenseaccount_id.id})
