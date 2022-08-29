# -*- coding: utf-8 -*-

from odoo import api, fields, models

class add_prm_vendor(models.TransientModel):
    _name = "add.prm.vendor"
    _inherit = "product.sample.wizard"
    _description = "Update Vendors"

    supplier_id = fields.Many2one(
        'res.partner',
        string="Supplier",
        required=True,
    )
    min_qty = fields.Float(string='Minimal quantity')
    delay = fields.Integer(string='Time of delivery')

    def _update_products(self, product_ids):
        """
        The method to prepare new vals for suppliers

        Args:
         * product_ids - product.template recordset

        Extra info:
         * Expected singleton
        """
        self.ensure_one()
        seller_ids = product_ids.mapped("seller_ids")
        if seller_ids:
            # to make sure existing seller_ids has higher priority then newly created
            seller_to_high_priority = seller_ids.filtered(lambda sel: sel.sequence <= 0)
            if seller_to_high_priority:
                seller_to_high_priority.write({"sequence": 1})
        supplier_info_dict = {
            'name': self.supplier_id.id,
            'min_qty': self.min_qty,
            'delay': self.delay,
            'sequence': 0,
        }
        values = {'seller_ids': [(0, 0, supplier_info_dict)],}
        product_ids.write(values)
