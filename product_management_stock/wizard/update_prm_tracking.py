# -*- coding: utf-8 -*-

from odoo import api, fields, models

class update_prm_tracking(models.TransientModel):
    _name = "update.prm.tracking"
    _inherit = "product.sample.wizard"
    _description = "Update tracking"

    @api.model
    def tracking_selection(self):
        """
        The method to return avaialble selection values for tracking
        """
        return self.env["product.template"]._fields["tracking"]._description_selection(self.env)

    tracking = fields.Selection(
        tracking_selection,
        string="New tracking",
        required=True,
    )

    def _update_products(self, product_ids):
        """
        The method to prepare new vals for tracking

        Args:
         * product_ids - product.template recordset

        Extra info:
         * Expected singleton
        """
        self.ensure_one()
        product_ids.write({"tracking": self.tracking})
        product_ids.onchange_tracking()
