from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SrGenerateSingleInvoice(models.TransientModel):
    _name = 'sr.generate.single.invoice'

    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    invoice_date = fields.Date('Invoice Date', default=fields.Date.context_today)
    journal_id = fields.Many2one('account.journal', 'journal', readonly=True)
    payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms')

    @api.model
    def default_get(self, vals):
        picking_ids = self.env[self.env.context.get('active_model')].browse(self.env.context.get('active_ids'))
        result = super(SrGenerateSingleInvoice, self).default_get(vals)
        if not picking_ids:
            return result
        else:
            if any(record.state in ('draft', 'waiting', 'confirmed', 'cancel') for record in picking_ids):
                raise UserError(_("You can generate invoice only for Ready and Done state pickings."))
            if len(set([record.partner_id.name for record in picking_ids])) != 1:
                raise UserError(_("Partner should be same to generate single invoice."))
            if len(set([record.picking_type_id.code for record in picking_ids])) != 1:
                raise UserError(_("You have selected mix incoming and outgoing pickings."))
            for record in picking_ids:
                if record.is_invoiced == True:
                    raise UserError(_("Selected Picking is already invoiced."))
            if picking_ids[0].picking_type_id.code == 'incoming':
                journal_id = self.env['account.journal'].search([('type', '=', 'purchase')])
            else:
                journal_id = self.env['account.journal'].search([('type', '=', 'sale')])
            result.update({
                'journal_id': journal_id.id,
                'partner_id': picking_ids[0].partner_id.id
            })
            return result

    def create_invoice(self):
        picking_ids = self.env[self.env.context.get('active_model')].browse(self.env.context.get('active_ids'))
        if self.journal_id.type == 'sale':
            val_list = []
            for record in picking_ids:
                for move in record.move_ids_without_package:
                    val_list.append((0, 0, {
                        'product_id': move.product_id.id,
                        'name': move.product_id.name,
                        'account_id': move.product_id.categ_id.property_account_income_categ_id.id,
                        'quantity': move.product_uom_qty,
                        'price_unit': move.created_sale_order_line_id.price_unit,
                        'tax_ids': [(6, 0, move.created_sale_order_line_id.tax_id.ids)],
                        'custom_move_id': move.id,
                        'sale_line_ids': [(6, 0, move.sale_line_id.ids)]
                    }))
                record.is_invoiced = True
            invoice_id = self.env['account.move'].create({
                'partner_id': self.partner_id.id,
                'invoice_date': self.invoice_date,
                'invoice_payment_term_id': self.payment_term_id.id,
                'journal_id': self.journal_id.id,
                'type': 'out_invoice',
                'invoice_user_id': self.env.uid,
                'invoice_line_ids': val_list,
                'custom_picking_ids': [(6, 0, picking_ids.ids)]
            })
        else:
            val_list = []
            for record in picking_ids:
                for move in record.move_ids_without_package:
                    print("==========move", move.purchase_line_id)
                    val_list.append((0, 0, {
                        'product_id': move.product_id.id,
                        'name': move.product_id.name,
                        'account_id': move.product_id.categ_id.property_account_expense_categ_id.id,
                        'quantity': move.product_uom_qty,
                        'price_unit': move.purchase_line_id.price_unit,
                        'tax_ids': [(6, 0, move.purchase_line_id.taxes_id.ids)],
                        'custom_move_id': move.id,
                        'purchase_line_id': move.purchase_line_id.id
                    }))
                record.is_invoiced = True
            invoice_id = self.env['account.move'].create({
                'partner_id': self.partner_id.id,
                'invoice_date': self.invoice_date,
                'invoice_payment_term_id': self.payment_term_id.id,
                'journal_id': self.journal_id.id,
                'type': 'in_invoice',
                'invoice_user_id': self.env.uid,
                'invoice_line_ids': val_list,
                'custom_picking_ids': [(6, 0, picking_ids.ids)]
            })
        return
