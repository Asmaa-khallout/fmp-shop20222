# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    invoice_status = fields.Selection(
        [('to_be_invoice', 'To Invoice'), ('partial_paid', 'Partial Paid'), ('posted', 'Fully Paid')],
        compute='compute_invoice_status')
    delivery_status = fields.Selection([('to_be_deliver', 'To Be Delivered'), ('partial_deliver', 'Partial Delivered'),
                                        ('delivered', 'Fully Delivered')], compute='compute_delivery_status')

    def custom_dummy_button(self):
        return

    def compute_invoice_status(self):
        for record in self:
            if record.invoice_ids:
                if all(a.state == "draft" for a in record.invoice_ids):
                    record.invoice_status = 'to_be_invoice'
                elif any(a.state == "draft" for a in record.invoice_ids) or any(a.state == "posted" for a in record.invoice_ids) and (a.amount_total == a.amount_residual for a in record.invoice_ids):
                    record.invoice_status = 'to_be_invoice'
                elif any(a.state == "draft" for a in record.invoice_ids) and any(a.amount_total == a.amount_residual for a in record.invoice_ids) and not any(a.state == "posted" for a in record.invoice_ids):
                    record.invoice_status = 'to_be_invoice'
                elif any(a.amount_residual > 0.00 for a in record.invoice_ids) and any(a.amount_residual < a.amount_total for a in record.invoice_ids) and any(a.state == "posted" for a in record.invoice_ids):
                    record.invoice_status = 'partial_paid'
                elif all(a.state == "posted" for a in record.invoice_ids) and all(a.amount_residual == 0.00 for a in record.invoice_ids):
                    record.invoice_status = "posted"
                else:
                    record.invoice_status = False
            else:
                record.invoice_status = False

    def compute_delivery_status(self):
        for record in self:
            print("=======record.picking_ids", record.picking_ids)
            if record.picking_ids:
                if all(a.state == "draft" for a in record.picking_ids) or all(a.state == "assigned" for a in record.picking_ids) or all(a.state == "confirmed" for a in record.picking_ids):
                    record.delivery_status = 'to_be_deliver'
                elif any(a.state == "draft" for a in record.picking_ids) or any(a.state == "assigned" for a in record.picking_ids) or any(a.state == "confirmed" for a in record.picking_ids) and not any(a.state == "done" for a in record.picking_ids):
                    record.delivery_status = 'to_be_deliver'
                elif all(a.state == "done" for a in record.picking_ids):record.delivery_status = 'delivered'
                elif any(a.state == "done" for a in record.picking_ids) and any(a.state == "assigned" for a in record.picking_ids):
                    record.delivery_status = "partial_deliver"
                elif any(a.state == "done" for a in record.picking_ids) and any(a.state == "confirmed" for a in record.picking_ids):
                    record.delivery_status = "partial_deliver"
                elif any(a.state == "done" for a in record.picking_ids) and any(a.state == "draft" for a in record.picking_ids):
                    record.delivery_status = "partial_deliver"
                elif any(a.state == "done" for a in record.picking_ids) and any(a.state == "cancel" for a in record.picking_ids) and not any(a.state == "confirmed" for a in record.picking_ids) and not any(a.state == "assigned" for a in record.picking_ids):
                    record.delivery_status = "delivered"
                else:
                    record.delivery_status = False
            else:
                record.delivery_status = False
