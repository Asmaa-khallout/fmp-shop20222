# -*- coding: utf-8 -*-

from odoo import api, fields, models

class update_prm_productionlocation(models.TransientModel):
    _name = "update.prm.productionlocation"
    _inherit = "product.sample.wizard"
    _description = "Update production location"

    productionlocation_id = fields.Many2one(
        "stock.location",
        string="New production location",
        domain=[('usage', 'like', 'production')],
        required=True,
    )

    def _update_products(self, product_ids):
        """
        The method to prepare new vals for production location

        Args:
         * product_ids - product.template recordset

        Extra info:
         * Expected singleton
        """
        self.ensure_one()
        product_ids.write({"property_stock_production": self.productionlocation_id.id})
