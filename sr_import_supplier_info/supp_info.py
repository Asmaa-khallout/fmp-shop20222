import tempfile
import binascii
import logging
from odoo.exceptions import Warning
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')


class gen_suppinfo(models.TransientModel):
    _name = "gen.suppinfo"

    file = fields.Binary('File')

    def import_fle(self):
        fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.file))
        fp.seek(0)
        values = {}
        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)
        for row_no in range(sheet.nrows):
            if row_no <= 0:
                fields = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
            else:
                line = list(
                    map(lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value),
                        sheet.row(row_no)))
                values.update({'vendor': line[0],
                               'product': line[1],
                               'delivery_time': line[2],
                               'quantity': line[3],
                               'price': line[4],
                               })
                res = self._create_product_suppinfo(values)
        return res

    def _create_product_suppinfo(self, val):
        name = self._find_vendor(val.get('vendor'))
        product_tmpl_id = self._find_product_template(val.get('product'))
        res = self.env['product.supplierinfo'].create({
            'name': name,
            'product_tmpl_id': product_tmpl_id,
            'product_name': self.env['product.template'].browse(product_tmpl_id).name,
            'min_qty': int(float(val.get('quantity'))),
            'price': val.get('price'),
            'delay': int(float(val.get('delivery_time')))
        })
        return res

    def _find_vendor(self, name):
        partner_search = self.env['res.partner'].search([('name', '=', name)])
        if not partner_search:
            raise Warning(_("%s Vendor Not Found") % name)
        return partner_search.id

    def _find_product_template(self, product):
        product_id = self.env['product.product'].search([('default_code', '=', product)])
        if product_id:
            product_tmpl_search = product_id.product_tmpl_id
        if not product_id:
            raise Warning(_(" %s code not found in system") % product)
        return product_tmpl_search.id
