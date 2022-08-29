# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
import sys
import tempfile
import binascii
import xlrd
import base64
import io
import csv
from itertools import product

TYPE2JOURNAL = {
    'customer': 'sale',
    'vendor': 'purchase',
    'customer_refund': 'sale',
    'vendor_refund': 'purchase',
}


class AccountMove(models.Model):
    _inherit = "account.move"

    sequence_custom = fields.Boolean('Custom Sequence')
    sequence_system = fields.Boolean('System Sequence')


class ImportInvoice(models.TransientModel):
    _name = 'import.invoice'
    _description = 'Import Invoice'

    file = fields.Binary('File')
    import_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select File', default='csv')
    invoice_stage_selection = fields.Selection([('draft', 'Draft Invoice'), ('open', 'Validate invoice')],
                                               string='Invoice Stage', default='draft')
    sequence_option = fields.Selection([('custom', 'Use sequence from Excel/CSV'), ('default', 'Use Default Sequence')],
                                       string='Sequnce option', default='default')
    import_product_by = fields.Selection([('name', 'Name'), ('code', 'Code'), ('barcode', 'Barcode')],
                                         string='Import Product By', default='name')
    import_customer_by = fields.Selection([('name', 'Name'), ('ref', 'Internal Reference')],
                                          string='Import Customer/Vendor By', default='name')
    import_account_by = fields.Selection([('file', 'From Excel/CSV File'), ('product', 'From Product')],
                                         string='Import Invoice Line Account By', default='product')
    import_invoice_by = fields.Selection(
        [('customer', 'Customer Invoice'), ('vendor', 'Vendor Invoice'), ('customer_refund', 'Customer Refund'),
         ('vendor_refund', 'Vendor Refund')], string='Import Invoice By', default='customer')

    def find_partner(self, customer):
        if not customer:
            return False
        if self.import_customer_by == 'name':
            partner_id = self.env['res.partner'].search([('name', '=', customer)])
        else:
            partner_id = self.env['res.partner'].search([('ref', '=', customer)])
        if partner_id:
            return partner_id.id
        else:
            raise UserError(_('%s Customer does not exist in system' % customer))

    def find_user(self, salesperson):
        if not salesperson:
            return False
        user_id = self.env['res.users'].search([('name', '=', salesperson)])
        if user_id:
            return user_id.id
        else:
            raise UserError(_('%s salesperson does not exist in system' % salesperson))

    def find_product(self, product):
        if self.import_product_by == 'name':
            product_id = self.env['product.product'].search([('name', '=', product)])
            if not product_id:
                raise UserError(_('Product with name %s does not exist in system' % product))
        elif self.import_product_by == 'code':
            product_id = self.env['product.product'].search([('default_code', '=', product)])
            if not product_id:
                raise UserError(_('Product with code %s does not exist in system' % product))

        else:
            product_id = self.env['product.product'].search([('barcode', '=', product)])
            if not product_id:
                raise UserError(_('Product with barcode %s does not exist in system' % product))
        return product_id.id

    def find_uom(self, uom):
        uom_id = self.env['uom.uom'].search([('name', '=', uom)])
        if uom_id:
            return uom_id.id
        else:
            raise UserError(_('%s Unit Of Measure does not exist in system' % uom))

    def find_payment_term(self, payment_term):
        payment_term_id = self.env['account.payment.term'].search([('name', '=', payment_term)])
        if payment_term_id:
            return payment_term_id.id
        else:
            raise UserError(_('%s Payment Terms does not exist in system' % payment_term))

    def _find_account_id(self, account):
        account_id = self.env['account.account'].search([('name', '=', account)])
        if not account_id:
            raise UserError(_('%s Account does not exist in system' % account))
        return account_id.id

    def _find_product_account_id(self, product):
        if self.import_product_by == 'name':
            product_id = self.env['product.product'].search([('name', '=', product)])
            if not product_id:
                raise UserError(_('Product with name %s does not exist in system' % product))
        elif self.import_product_by == 'code':
            product_id = self.env['product.product'].search([('default_code', '=', product)])
            if not product_id:
                raise UserError(_('Product with code %s does not exist in system' % product))

        else:
            product_id = self.env['product.product'].search([('barcode', '=', product)])
            if not product_id:
                raise UserError(_('Product with barcode %s does not exist in system' % product))
        if self.import_invoice_by == 'customer' or self.import_invoice_by == 'customer_refund':
            return product_id.categ_id.property_account_income_categ_id.id
        elif self.import_invoice_by == 'vendor' or self.import_invoice_by == 'vendor_refund':
            return product_id.categ_id.property_account_expense_categ_id.id

    def create_invoice_line(self, values):
        invoice_line_dict = {}
        tax_ids = []
        if values.get('tax'):
            type_tax_use = ''
            taxes = values.get('tax').split(',')
            for name in taxes:
                if self.import_invoice_by == 'customer' or self.import_invoice_by == 'customer_refund':
                    type_tax_use = 'sale'
                else:
                    type_tax_use = 'purchase'
                tax = self.env['account.tax'].search([('name', '=', name), ('type_tax_use', '=', type_tax_use)])
                if not tax:
                    raise Warning(_('"%s" Tax not in your system') % name)
                tax_ids.append(tax.id)

        if self.import_account_by == 'file':
            invoice_line_dict = {
                'product_id': self.find_product(values.get('product')),
                'name': values.get('description'),
                'quantity': values.get('quantity'),
                'product_uom_id': self.find_uom(values.get('uom')),
                'price_unit': values.get('price'),
                'account_id': self._find_account_id(values.get('account')),
                'tax_ids': ([(6, 0, tax_ids)])
            }
        else:
            invoice_line_dict = {
                'product_id': self.find_product(values.get('product')),
                'name': values.get('description'),
                'quantity': values.get('quantity'),
                'product_uom_id': self.find_uom(values.get('uom')),
                'price_unit': values.get('price'),
                'account_id': self._find_product_account_id(values.get('product')),
                'tax_ids': ([(6, 0, tax_ids)])
            }
        print("===========invoice_line_dict", invoice_line_dict)
        return invoice_line_dict

    def _default_journal(self):
        inv_type = self.import_invoice_by
        inv_types = inv_type if isinstance(inv_type, list) else [inv_type]
        company_id = self._context.get('company_id', self.env.user.company_id.id)
        domain = [
            ('type', 'in', [TYPE2JOURNAL[ty] for ty in inv_types if ty in TYPE2JOURNAL]),
            ('company_id', '=', company_id),
        ]
        return self.env['account.journal'].search(domain, limit=1)

    def create_invoice(self, value):
        invoice_list_id = []
        invoice_id = self.env['account.move'].search([('name', '=', value.get('name'))])
        if invoice_id:
            if invoice_id.partner_id.name == value.get('customer'):
                if invoice_id.user_id.name == (value.get('salesperson') or False):
                    invoice_id.write({'invoice_line_ids': [(0, 0, self.create_invoice_line(value))]})
                else:
                    raise UserError(_('Sales Person is different for %s, \n Please define same' % value.get('name')))
            else:
                raise UserError(_('Customer is different for %s, \n Please define same' % value.get('name')))
        else:
            if self.import_invoice_by == 'customer':
                type = 'out_invoice'
            elif self.import_invoice_by == 'vendor':
                type = 'in_invoice'
            elif self.import_invoice_by == 'customer_refund':
                type = 'out_refund'
            else:
                type = 'in_refund'

            if self.sequence_option == 'default':
                journal = self._default_journal()
                if journal.sequence_id:
                    sequence = journal.sequence_id
                    name = sequence.with_context(
                        ir_sequence_date=datetime.today().date().strftime("%Y-%m-%d")).next_by_id()
                else:
                    raise UserError(_('Please define a sequence on the journal.'))
            else:
                name = value.get('name')
            order_id = self.env['account.move'].create({
                'name': name,
                'partner_id': self.find_partner(value.get('customer')),
                'invoice_date': value.get('date'),
                'user_id': self.find_user(value.get('salesperson')),
                'invoice_payment_term_id': self.find_payment_term(value.get('payment_term')),
                'type': type,
                'journal_id': self._default_journal().id,
                'sequence_custom': True if self.sequence_option == 'custom' else False,
                'sequence_system': True if self.sequence_option == 'default' else False,
                'invoice_line_ids': [(0, 0, self.create_invoice_line(value))]
            })

    def import_invoices(self):
        try:
            if self.import_option == 'xls':
                fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
                fp.write(binascii.a2b_base64(self.file))
                fp.seek(0)
                values = {}
                workbook = xlrd.open_workbook(fp.name)
                sheet = workbook.sheet_by_index(0)
                for row_no in range(sheet.nrows):
                    val = {}
                    if row_no <= 0:
                        fields = list(map(lambda row: row.value.encode('utf-8'), sheet.row(row_no)))
                    else:
                        line = list(map(lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(
                            row.value), sheet.row(row_no)))
                        date_tuple = xlrd.xldate_as_tuple(float(line[2]), workbook.datemode)
                        date = datetime(*date_tuple).strftime('%Y-%m-%d')
                        values.update({'name': line[0],
                                       'customer': line[1],
                                       'date': date,
                                       'payment_term': line[3],
                                       'salesperson': line[4],
                                       'product': line[5],
                                       'description': line[6],
                                       'account': line[7],
                                       'quantity': line[8],
                                       'uom': line[9],
                                       'price': line[10],
                                       'tax': line[11],
                                       })
                        res = self.create_invoice(values)
            else:
                keys = ['name', 'customer', 'date', 'payment_term', 'salesperson', 'product', 'description', 'account',
                        'quantity', 'uom', 'price', 'tax']
                try:
                    csv_data = base64.b64decode(self.file)
                    data_file = io.StringIO(csv_data.decode("utf-8"))
                    data_file.seek(0)
                    file_reader = []
                    values = {}
                    csv_reader = csv.reader(data_file, delimiter=',')
                    file_reader.extend(csv_reader)
                except:
                    raise Warning(_("Invalid file!"))
                for i in range(len(file_reader)):
                    field = list(map(str, file_reader[i]))
                    values = dict(zip(keys, field))
                    if values:
                        if i == 0:
                            continue
                        else:
                            values.update({
                                'name': field[0],
                                'customer': field[1],
                                'date': field[2],
                                'payment_term': field[3],
                                'salesperson': field[4],
                                'product': field[5],
                                'description': field[6],
                                'account': field[7],
                                'quantity': field[8],
                                'uom': field[9],
                                'price': field[10],
                                'tax': field[11],
                            })
                            res = self.create_invoice(values)
        except Exception as e:
            raise UserError(_(e))
