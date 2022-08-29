# -*- coding: utf-8 -*-

from odoo import api, fields, models

class update_prm_alternatives(models.TransientModel):
    _name = "update.prm.alternatives"
    _inherit = "product.sample.wizard"
    _description = "Update public categories"

    alternative_to_add_ids = fields.Many2many(
        "product.template",
        "product_template_add_prm_public_categories_rel_table",
        "product_template_id",
        "update_prm_alternatives_id",
        string="Add alternatives",
    )
    alternative_to_exclude_ids = fields.Many2many(
        "product.template",
        "product_template_exclude_prm_public_categories_rel_table",
        "product_template_id",
        "update_prm_alternatives_id",
        string="Remove alternatives",
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
        if self.alternative_to_add_ids:
            to_add = []
            for alter in self.alternative_to_add_ids.ids:
                to_add.append((4, alter))
            product_ids.write({"alternative_product_ids": to_add,})
        if self.alternative_to_exclude_ids:
            to_exclude = []
            for alter in self.alternative_to_exclude_ids.ids:
                to_exclude.append((3, alter))
            product_ids.write({"alternative_product_ids": to_exclude,})
