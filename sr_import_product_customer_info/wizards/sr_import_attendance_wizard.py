from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.misc import format_date as odoo_format_date, get_lang
import datetime
import tempfile
import binascii
import xlrd
import base64
import io
import csv

class srImportProductCustomerInfo(models.TransientModel):
    _name = 'sr.import.product.customer.info'

    import_file = fields.Binary('Select File')

    def _find_product(self, product):
        product_id = self.env['product.product'].search([('default_code', '=', product)])
        if not product_id:
            raise UserError(_('Product name "%s" is not available in system' % product))
        else:
            return product_id

    def _find_partner(self, partner):
        partner_id = self.env['res.partner'].search([('name', '=', partner)])
        if not partner_id:
            raise UserError(_('partner name "%s" is not available in system' % partner))
        else:
            return partner_id

    def _find_company(self, company):
        company_id = self.env['res.company'].search([('name', '=', company)])
        if not company_id:
            raise UserError(_('Company name "%s" is not available in system' % company))
        else:
            return company_id

    def import_data(self, data):
        if not data.get('product'):
            raise Warning('Please provide Product')
        if not data.get('partner'):
            raise Warning('Please provide Customer')

        product_id = self._find_product(data.get('product'))
        partner_id = self._find_partner(data.get('partner'))
        company_id = self._find_company(data.get('company'))
        info_line = self.env['product.customer.info'].search([('partner_id', '=', partner_id.id), ('product_id', '=', product_id.id)])
        if info_line:
            for line in info_line:
                line.write({
                    'customer_product_name': data.get('customer_product_name'),
                    'customer_product_code': data.get('customer_product_code'),
                })
        else:
            new_id = self.env['product.customer.info'].create({
                'partner_id': partner_id.id,
                'customer_product_name': data.get('customer_product_name'),
                'customer_product_code': data.get('customer_product_code'),
                'product_id': product_id.id,
                'company_id': company_id.id,
                'product_tmpl_id': product_id.product_tmpl_id.id
            })
        return True

    def import_product_customer_info(self):
        try:
            fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.import_file))
            fp.seek(0)
            values = {}
            workbook = xlrd.open_workbook(fp.name)
            sheet = workbook.sheet_by_index(0)
            for row_no in range(sheet.nrows):
                val = {}
                if row_no <= 0:
                    fields = list(map(lambda row: row.value.encode('utf-8'), sheet.row(row_no)))
                else:
                    line = list(
                        map(lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value),
                            sheet.row(row_no)))
                    values.update({
                        'product': line[0],
                        'partner': line[1],
                        'customer_product_name': line[2],
                        'customer_product_code': line[3],
                        'company': line[4]
                    })
                    self.import_data(values)
        except Exception as e:
            raise UserError(_(e))
