# -*- coding: utf-8 -*-

from odoo import api, fields, models

class update_prm_routes(models.TransientModel):
    _name = "update.prm.routes"
    _inherit = "product.sample.wizard"
    _description = "Update logistic routes"

    routes_to_add_ids = fields.Many2many(
        "stock.location.route",
        "stock_location_route_add_prm_routes_rel_table",
        "stock_location_route_id",
        "update_prm_routes_id",
        domain=[('product_selectable', '=', True)],
        string="Add routes",
    )
    routes_to_exclude_ids = fields.Many2many(
        "stock.location.route",
        "stock_location_route_exclude_prm_routes_rel_table",
        "stock_location_route_id",
        "update_prm_routes_id",
        domain=[('product_selectable', '=', True)],
        string="Remove routes",
    )

    def _update_products(self, product_ids):
        """
        The method to prepare new vals for routes

        Args:
         * product_ids - product.template recordset

        Extra info:
         * Expected singleton
        """
        self.ensure_one()
        if self.routes_to_add_ids:
            to_add = []
            for alter in self.routes_to_add_ids.ids:
                to_add.append((4, alter))
            product_ids.write({"route_ids": to_add,})
        if self.routes_to_exclude_ids:
            to_exclude = []
            for alter in self.routes_to_exclude_ids.ids:
                to_exclude.append((3, alter))
            product_ids.write({"route_ids": to_exclude,})
