# -*- coding: utf-8 -*-

from odoo import api, fields, models

class update_prm_invoicepolicy(models.TransientModel):
    _name = "update.prm.invoicepolicy"
    _inherit = "product.sample.wizard"
    _description = "Update Invoice Policy"

    invoice_policy = fields.Selection(
        [
            ('order', 'Ordered quantities'),
            ('delivery', 'Delivered quantities')
        ],
        string="New invoice policy",
        required=True,
    )

    def _update_products(self, product_ids):
        """
        The method to prepare new vals invoice_policy

        Args:
         * product_ids - product.template recordset

        Extra info:
         * Expected singleton
        """
        self.ensure_one()
        product_ids.write({"invoice_policy": self.invoice_policy})
