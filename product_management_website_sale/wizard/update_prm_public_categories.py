# -*- coding: utf-8 -*-

from odoo import api, fields, models

class update_prm_public_categories(models.TransientModel):
    _name = "update.prm.public_categories"
    _inherit = "product.sample.wizard"
    _description = "Update public categories"

    categories_to_add_ids = fields.Many2many(
        "product.public.category",
        "product_public_category_add_prm_public_categories_rel_table",
        "product_public_category_id",
        "update_prm_public_categories_id",
        string="Add public categories",
    )
    categories_to_exclude_ids = fields.Many2many(
        "product.public.category",
        "product_public_category_exclude_prm_public_categories_rel_table",
        "product_public_category_id",
        "update_prm_public_categories_id",
        string="Remove public categories",
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
        if self.categories_to_add_ids:
            to_add = []
            for categ in self.categories_to_add_ids.ids:
                to_add.append((4, categ))
            product_ids.write({"public_categ_ids": to_add,})
        if self.categories_to_exclude_ids:
            to_exclude = []
            for categ in self.categories_to_exclude_ids.ids:
                to_exclude.append((3, categ))
            product_ids.write({"public_categ_ids": to_exclude,})
