# -*- coding: utf-8 -*-

from odoo import api, fields, models

class update_prm_purchasetax(models.TransientModel):
    _name = "update.prm.purchasetax"
    _inherit = "product.sample.wizard"
    _description = "Update sale taxes"

    taxes_to_add_ids = fields.Many2many(
        "account.tax",
        "account_tax_add_prm_purchasetax_rel_table",
        "account_tax_id",
        "update_prm_purchasetax_id",
        domain=[('type_tax_use', '=', 'purchase')],
        string="Add vendor taxes",
    )
    taxes_to_exclude_ids = fields.Many2many(
        "account.tax",
        "account_tax_exclude_prm_purchasetax_rel_table",
        "account_tax_id",
        "update_prm_purchasetax_id",
        domain=[('type_tax_use', '=', 'purchase')],
        string="Remove vendor taxes",
    )

    def _update_products(self, product_ids):
        """
        The method to prepare new vals for sale taxes

        Args:
         * product_ids - product.template recordset

        Extra info:
         * Expected singleton
        """
        self.ensure_one()
        if self.taxes_to_add_ids:
            to_add = []
            for alter in self.taxes_to_add_ids.ids:
                to_add.append((4, alter))
            product_ids.write({"supplier_taxes_id": to_add,})
        if self.taxes_to_exclude_ids:
            to_exclude = []
            for alter in self.taxes_to_exclude_ids.ids:
                to_exclude.append((3, alter))
            product_ids.write({"supplier_taxes_id": to_exclude,})
