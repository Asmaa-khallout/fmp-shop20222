# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

ACTIVATION_STATES = [
    ('active', 'Active'),
    ('inactive', 'Inactive')]


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    numero_siret = fields.Char("Siret")
    name_shop = fields.Char('Name of shop')
    activation_state = fields.Selection(ACTIVATION_STATES, string='Activation state')
    # attachement_activation_ids = fields.Many2many("ir.attachment" ,string="Attachment for activation")
    attachment_activation_count = fields.Integer('Attachment Count',
                                                 compute='_compute_attachment_activation_count')

    description_activation = fields.Text("Description activation")

    def _compute_attachment_activation_count(self):
        for rec in self:
            attachments = self.env['ir.attachment'].search_count(
                [('res_model', '=', 'res.partner'), ('res_id', '=', rec.id), ('file_activation', '=', True)])
            rec.attachment_activation_count = attachments

    def action_show_attachments_activation(self):
        return {
            'name': _('Attachments'),
            'view_mode': 'kanban,form',
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'domain': [('res_model', '=', 'res.partner'), ('res_id', '=', self.id), ('file_activation', '=', True)]
        }

    def activate_portal_user(self):
        # Send activation email to new user
        related_user_id = self.env['res.users'].search([('partner_id', '=', self.id)], limit=1)
        if related_user_id:
            user_mail_template = self.env.ref('fmp_activation_user.user_activation_mail_template_for_active_user',
                                              raise_if_not_found=False)
            update = self.write({'activation_state': 'active'})
            if user_mail_template:
                user_mail_template.sudo().send_mail(related_user_id.id, force_send=True)
        else:
            raise UserError(_("Related user not found!"))

    def deactivate_portal_user(self):
        # Send deactivation email to new user
        related_user_id = self.env['res.users'].search([('partner_id', '=', self.id)], limit=1)
        if related_user_id:
            user_mail_template = self.env.ref('fmp_activation_use.user_activation_mail_template_for_deactive_user',
                                              raise_if_not_found=False)
            update = self.write({'activation_state': 'inactive'})
            if user_mail_template:
                user_mail_template.sudo().send_mail(related_user_id.id, force_send=True)
        else:
            raise UserError(_("Related user not found!"))
