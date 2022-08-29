# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    auto_print_label_state = fields.Selection([
            ('not_relevant', 'Not Relevant'),
            ('generated_label', 'Generated Label'), 
            ], 'Label State',
        default='not_relevant', required=True,
        help="It specifies if the label was printed for this delivery")

    def create_package_and_label(self):
        Package = self.env['stock.quant.package']
        for record in self:
            move_lines = record.move_line_ids.filtered(
                lambda r: not r.result_package_id)
            if move_lines:
                #warehouse = record.location_id.get_warehouse()
                #default_weight = warehouse.default_package_weight
                package = Package.create({
                    'shipping_weight': record.weight or 0
                    })
                move_lines.write({'result_package_id': package.id})
            if record.carrier_id:
                record.send_to_shipper()
                self.env.cr.commit()
        
    def send_to_shipper(self):
        self.ensure_one()
        new_label = self.env.context.get('new_label')
        if self.auto_print_label_state != 'generated_label' or new_label:
            Package = self.env['stock.quant.package']
            default_weight = self.location_id.warehouse_id.default_package_weight
            package = Package.create({
                'shipping_weight': self.shipping_weight or default_weight
                })
            self.move_line_ids.write({'result_package_id': package.id})
            super().send_to_shipper()
            self.auto_print_label_state = 'generated_label'
