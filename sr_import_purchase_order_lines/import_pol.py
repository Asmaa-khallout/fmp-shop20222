from odoo import api, fields, models, _, exceptions
from datetime import datetime
from odoo.exceptions import Warning
import binascii
import tempfile
from tempfile import TemporaryFile
from odoo.exceptions import UserError, ValidationError
import logging
from odoo.tools import ustr

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


class import_po_line_wizard(models.TransientModel):
    _name = 'import.po.line.wizard'
    purchase_order_file = fields.Binary(string="Select File")

    def import_pol(self):
        fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.purchase_order_file))
        fp.seek(0)
        values = {}
        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)
        product_obj = self.env['product.product']
        for row_no in range(sheet.nrows):
            val = {}
            if row_no <= 0:
                fields = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
            else:
                line = list(
                    map(lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or ustr(row.value),
                        sheet.row(row_no)))
                res = self.create_po_line(line)
        return res

    def create_po_line(self, line):
        purchase_order_brw = self.env['purchase.order'].browse(self._context.get('active_id'))
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        product = self.env['product.product'].search([('default_code', '=', line[0])])
        if not product:
            raise UserError(_('%s code not found in the system' % line[0]))
        currency = self.env['res.currency'].search([('name', '=', line[3])])
        if not currency:
            raise UserError(_('%s Currency not found in the system' % currency))
        res = self.env['purchase.order.line'].create({
            'product_id': product.id,
            'name': product.name,
            'date_planned': current_time,
            'product_uom': product.uom_id.id,
            'product_qty': line[2],
            'price_unit': line[1],
            'order_id': self._context.get('active_id')
        })
        return res
