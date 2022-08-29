# -*- coding: utf-8 -*-

from odoo import api, fields, models

class update_prm_pricedifferenceaccount(models.TransientModel):
    _name = "update.prm.pricedifferenceaccount"
    _inherit = "product.sample.wizard"
    _description = "Update price difference account"

    pricedifferenceaccount_id = fields.Many2one(
        "account.account",
        string="New expense account",
        domain=[('deprecated', '=', False)],
        required=True,
    )

    def _update_products(self, product_ids):
        """
        The method to prepare new vals for price difference account

        Args:
         * product_ids - product.template recordset

        Extra info:
         * Expected singleton
        """
        self.ensure_one()
        product_ids.write({"property_account_creditor_price_difference": self.pricedifferenceaccount_id.id})
