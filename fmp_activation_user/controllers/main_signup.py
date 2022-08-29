# -*- coding: utf-8 -*-
import logging
import werkzeug
import base64
import datetime

from odoo import http, _
from odoo.addons.web.controllers.main import Home
from odoo.exceptions import UserError
from odoo.addons.auth_signup.models.res_partner import SignupError
from odoo.http import request

_logger = logging.getLogger(__name__)
SIGN_UP_REQUEST_PARAMS = {'db', 'login', 'debug', 'token', 'message', 'error', 'scope', 'mode',
                          'redirect', 'redirect_hostname', 'email', 'name', 'partner_id',
                          'password', 'confirm_password', 'city', 'country_id', 'lang','phone','mobile','numero_siret','name_shop','activation_state','company_type','vat','street','street2','zip'}

class AuthSignupHome(Home):

    def insert_attachment(self,record, files):
        list_data = []
        for file in files:
            attached_file = file.read()
            attachment_value = {
                'name': file.filename,
                'file_activation':True,
                'datas':   base64.encodebytes(attached_file),
                'res_model': 'res.partner',
                'res_id': record,
            }
            attachment_id = request.env['ir.attachment'].sudo().create(attachment_value)

    def _prepare_signup_values(self, qcontext):
        values = { key: qcontext.get(key) for key in ('login', 'name', 'password','phone','mobile','numero_siret','name_shop','vat','street','street2','zip','city','country_id') }
        qcontext['zip_2']=values['zip']
        country = 'country_id' in values and values['country_id'] != '' and request.env['res.country'].browse(int(values['country_id']))
        qcontext['country'] = country and country.exists() or ''
        if(values['country_id']):
            values['country_id'] = int(values['country_id'])
        values['activation_state']="inactive"
        company_type="person"
        if(values['numero_siret']):
            company_type = "company"
        values['company_type'] = company_type
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '')
        if lang in supported_lang_codes:
            values['lang'] = lang
        return values

    def get_auth_signup_qcontext(self):
        """ Shared helper returning the rendering context for signup and reset password """
        qcontext = {k: v for (k, v) in request.params.items() if k in SIGN_UP_REQUEST_PARAMS}
        qcontext.update(self.get_auth_signup_config())
        if not qcontext.get('token') and request.session.get('auth_signup_token'):
            qcontext['token'] = request.session.get('auth_signup_token')
        if qcontext.get('token'):
            try:
                # retrieve the user info (name, login or email) corresponding to a signup token
                token_infos = request.env['res.partner'].sudo().signup_retrieve_info(qcontext.get('token'))
                for k, v in token_infos.items():
                    qcontext.setdefault(k, v)
            except:
                qcontext['error'] = _("Invalid signup token")
                qcontext['invalid_token'] = True
        return qcontext


    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        qcontext['countries'] = request.env['res.country'].sudo().search([])
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                if qcontext.get('token'):
                    User = request.env['res.users']
                    user_sudo = User.sudo().search(
                        User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                    )
                else:
                    user_sudo = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))], limit=1)
                try:
                    if (kw.get('attachement_activation_ids', False)):
                        attachment_ids = request.httprequest.files.getlist('attachement_activation_ids')
                        self.insert_attachment(user_sudo.partner_id, attachment_ids)
                except Exception as e:
                    _logger.info("erreeeur %s" %(e))
                    pass
                admin = request.env.ref("base.user_admin").sudo()
                todos = {
                    'res_id': user_sudo.partner_id.id,
                    'res_model_id': 84,
                    'user_id': admin.id,
                    'summary': (_("Activation for User: %s" %(user_sudo.name))),
                    'note': (_("New user account activated")),
                    'activity_type_id': 4,
                    'date_deadline': datetime.date.today(),
                }

                request.env['mail.activity'].sudo().create(todos)
                template_admin = request.env.ref('fmp_activation_user.user_activation_mail_template_for_admin', raise_if_not_found=False)
                if template_admin:
                    template_admin.sudo().send_mail(user_sudo.id, force_send=True)
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.args[0]
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    error =_("Could not create a new account.")
                    _logger.info(str(e))

                    if("Le numéro de TVA" in str(e)):
                        error = _("%s" %e)
                    qcontext['error'] = error

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response