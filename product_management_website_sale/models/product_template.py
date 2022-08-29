#coding: utf-8

from odoo import api, models
from odoo.tools.safe_eval import safe_eval


class product_template(models.Model):
    """
    Re-write to implement methods needed by js interface
    """
    _inherit = "product.template"

    @api.model
    def return_eshop_categories_hierarchy(self):
        """
        The method to return eshop categories in jstree format

        Methods:
         * _return_eshop_categories_recursive

        Returns:
         * list of folders dict with keys:
           ** id
           ** text - folder_name
           ** icon
           ** children - array with the same keys
        """
        Config = self.env['ir.config_parameter'].sudo()
        need_categories = safe_eval(Config.get_param("product_management_eshop_categories_option", "False"))
        res = []
        if need_categories:
            self = self.with_context(lang=self.env.user.lang)
            categories = self.env["product.public.category"].search([("parent_id", "=", False)])
            for category in categories:
                res.append(self._return_eshop_categories_recursive(category))
        return res

    @api.model
    def _return_eshop_categories_recursive(self, category):
        """
        The method to go by all categories recursively to prepare their list in js_tree format

        Args:
         * category - product.public.category instance
        """
        res = {
            "text": category.name,
            "id": category.id,
        }
        child_res = []
        child_ids = self.env["product.public.category"].search([("id", "in", category.child_id.ids)])
        for child in child_ids:
            child_res.append(self._return_eshop_categories_recursive(child))
        res.update({"children": child_res})
        return res