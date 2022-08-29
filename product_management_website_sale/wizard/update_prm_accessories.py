# -*- coding: utf-8 -*-

from odoo import api, fields, models

class update_prm_accessories(models.TransientModel):
    _name = "update.prm.accessories"
    _inherit = "product.sample.wizard"
    _description = "Update public categories"

    accessories_to_add_ids = fields.Many2many(
        "product.product",
        "product_product_add_prm_public_categories_rel_table",
        "product_product_id",
        "update_prm_accessories_id",
        string="Add accessories",
    )
    accessories_to_exclude_ids = fields.Many2many(
        "product.product",
        "product_product_exclude_prm_public_categories_rel_table",
        "product_product_id",
        "update_prm_accessories_id",
        string="Remove accessories",
    )

    def _update_products(self, product_ids):
        """
        The method to prepare new vals for public categories

        Args:
         * product_ids - product.template recordset

        Extra info:
         * Expected singleton
        """
        self.ensure_one()
        if self.accessories_to_add_ids:
            to_add = []
            for alter in self.accessories_to_add_ids.ids:
                to_add.append((4, alter))
            product_ids.write({"accessory_product_ids": to_add,})
        if self.accessories_to_exclude_ids:
            to_exclude = []
            for alter in self.accessories_to_exclude_ids.ids:
                to_exclude.append((3, alter))
            product_ids.write({"accessory_product_ids": to_exclude,})
