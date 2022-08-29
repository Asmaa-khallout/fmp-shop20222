from odoo import api, fields, models, _
from odoo.exceptions import Warning
import binascii
import tempfile
import xlrd
from tempfile import TemporaryFile
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)
import io

try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')
try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class order_line_wizard(models.TransientModel):
    _name = 'order.line.wizard'

    sale_order_file = fields.Binary(string="Select File")

    def import_sol(self):
        try:
            fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.sale_order_file))
            fp.seek(0)
            values = {}
            workbook = xlrd.open_workbook(fp.name)
            sheet = workbook.sheet_by_index(0)
        except Exception:
            raise Warning(_("Please select any file or You have selected invalid file"))

        for row_no in range(sheet.nrows):
            val = {}
            if row_no <= 0:
                fields = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
            else:
                line = list(
                    map(lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value),
                        sheet.row(row_no)))
                res = self.create_order_line(line)
        return res

    def create_order_line(self, line):
        sale_order_brw = self.env['sale.order'].browse(self._context.get('active_id'))
        tax = False
        if line[0] and line[1]:
            raise Warning(
                _("You have given value for customer product code and internal reference! \n Please Use Any one"))
        if line[0] and not line[1]:
            product_info = self.env['product.customer.info'].search(
                [('customer_product_code', '=', line[0]), ('partner_id', '=', sale_order_brw.partner_id.id)])
            if not product_info:
                raise Warning(_("Customer product code not found [%s]" % line[0]))
            if len(product_info) > 1:
                raise Warning(_("We found multiple product with [%s] customer product code " % line[0]))
            product = product_info.product_id
        if not line[0] and line[1]:
            product = self.env['product.product'].search([('default_code', '=', line[1])])
            if not product:
                raise Warning(_("Internal Reference not found [%s]" % line[1]))
            if len(product) > 1:
                raise Warning(_("We found multiple product with [%s] Internal reference " % line[1]))
        if sale_order_brw.partner_id.property_account_position_id.name == 'Domestique - France':
            tax = self.env['account.tax'].search([('name', '=', 'TVA collectée (vente) 20,0%')])
        order_lines = self.env['sale.order.line'].create({
            'order_id': sale_order_brw.id,
            'product_id': product.id,
            'name': product.name,
            'product_uom_qty': line[2],
            'product_uom': product.uom_id.id,
            'price_unit': line[3] if line[3] else product.lst_price,
            'tax_id': [(6, 0, tax.ids)]
        })
        return True
