#-*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

ACTIVATION_STATES = [
    ('active','Active'),
    ('inactive','Inactive')
]

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    
    @api.constrains('vat', 'country_id')
    def check_vat(self):
        # The context key 'no_vat_validation' allows you to store/set a VAT number without doing validations.
        # This is for API pushes from external platforms where you have no control over VAT numbers.
        if self.env.context.get('no_vat_validation'):
            return
        else:
            return

#         for partner in self:
#             country = partner.commercial_partner_id.country_id
#             if partner.vat and self._run_vat_test(partner.vat, country, partner.is_company) is False:
#                 partner_label = _("partner [%s]", partner.name)
#                 msg = partner._build_vat_error_message(country and country.code.lower() or None, partner.vat, partner_label)
#                 raise ValidationError(msg)


    activation_state = fields.Selection(ACTIVATION_STATES, string='Activation state')

    def activate_portal_user(self):
        #Send activation email to new user
        related_user_id = self.env['res.users'].search([('login','=',self.email)], limit=1)
        if related_user_id:
            user_mail_template = self.env.ref('fmp-contact_activation.user_activation_mail_template_for_active_user', 
                raise_if_not_found=False)
            if user_mail_template:
                user_mail_template.sudo().send_mail(related_user_id.id, force_send=True)
            return self.write({'activation_state':'active'})
        else:
            raise UserError(_("Related user not found!"))


    def deactivate_portal_user(self):
        #Send deactivation email to new user
        related_user_id = self.env['res.users'].search([('login','=',self.email)], limit=1)
        if related_user_id:        
            user_mail_template = self.env.ref('fmp-contact_activation.user_activation_mail_template_for_deactive_user', 
                raise_if_not_found=False)
            if user_mail_template:
                user_mail_template.sudo().send_mail(related_user_id.id, force_send=True)
            return self.write({'activation_state':'inactive'})
        else:
            raise UserError(_("Related user not found!"))

