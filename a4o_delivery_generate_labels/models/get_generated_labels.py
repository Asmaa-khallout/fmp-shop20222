# This file is part of an Adiczion's Module.
# The COPYRIGHT and LICENSE files at the top level of this repository
# contains the full copyright notices and license terms.
from odoo import fields, models, _
from odoo.tools import pdf
from odoo.exceptions import UserError
import base64
import logging

_logger = logging.getLogger(__name__)

 
class GetGeneratedLabels(models.TransientModel):
    _name = 'get.generated.labels'
    _description = 'Download Generated labels Wizard'

    labels_data = fields.Binary('Labels File', readonly=True)
    filename = fields.Char(string='Filename', size=256, readonly=True)

    def _prepare_domain(self, model_name, ids):
        company = self.env.context.get('company_id', self.env.user.company_id)
        domain = [
            ('res_model', '=', model_name),
            ('res_id', 'in', ids),
            ]
        if company.all_attachments_on_pdf:
            prefix = _('Label_')
            domain.append(('datas_fname', 'like', prefix))
        return domain

    def _get_all_labels(self, model_name, ids):
        domain = self._prepare_domain(model_name, ids)
        attachments = self.env['ir.attachment'].search(domain)
        if not attachments:
            raise UserError(_('No labels found on the selected packages. '
                'It may have been impossible to create them. '
                'Check by manual creation.'))
        return pdf.merge_pdf([
                base64.decodebytes(a.datas)
                for a in attachments
                ])

    def _create_package_and_label(self, model_name, ids):
        Picking = self.env[model_name]
        to_generate = []
        for id_ in ids:
            domain = self._prepare_domain(model_name, [id_])
            attachments = self.env['ir.attachment'].search(domain)
            if not attachments:
                to_generate.append(id_)
        if to_generate:
            pickings = Picking.browse(to_generate)
            pickings.create_package_and_label()

    def retrieve_labels(self):
        model_name = self._context.get('active_model')
        active_ids = self._context.get('active_ids')
        if not active_ids:
            return
        self._create_package_and_label(model_name, active_ids)
        labels = self._get_all_labels(model_name, active_ids)

        result = self.create({
            'labels_data': base64.b64encode(labels),
            'filename': _('Labels.pdf'),
            })

        action = {
            'name': 'Labels',
            'type': 'ir.actions.act_url',
            'url': "web/content/?model=get.generated.labels"
                    "&id=%s"
                    "&filename_field=filename"
                    "&field=labels_data"
                    "&download=true"
                    "&filename=%s" % (result.id, result.filename),
            'target': 'self',
            }
        return action
