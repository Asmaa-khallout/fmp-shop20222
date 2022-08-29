# -*- coding: utf-8 -*-

from odoo import api, fields, models

class update_prm_purchase_policy(models.TransientModel):
    _name = "update.prm.purchase.policy"
    _inherit = "product.sample.wizard"
    _description = "Update Purchase Policy"

    purchase_method = fields.Selection(
        [
            ('purchase', 'On ordered quantities'),
            ('receive', 'On received quantities'),
        ],
        string="New type",
    )

    def _update_products(self, product_ids):
        """
        The method to prepare new vals purchase_method

        Args:
         * product_ids - product.template recordset

        Extra info:
         * Expected singleton
        """
        self.ensure_one()
        product_ids.write({"purchase_method": self.purchase_method})
