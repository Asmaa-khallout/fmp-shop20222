# -*- coding: utf-8 -*-

from odoo import api, fields, models

class update_prm_inventorylocation(models.TransientModel):
    _name = "update.prm.inventorylocation"
    _inherit = "product.sample.wizard"
    _description = "Update inventory location"

    inventorylocation_id = fields.Many2one(
        "stock.location",
        string="New inventory location",
        domain=[('usage', 'like', 'inventory')],
        required=True,
    )

    def _update_products(self, product_ids):
        """
        The method to prepare new vals for inventory location

        Args:
         * product_ids - product.template recordset

        Extra info:
         * Expected singleton
        """
        self.ensure_one()
        product_ids.write({"property_stock_inventory": self.inventorylocation_id.id})
