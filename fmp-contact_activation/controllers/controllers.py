#-*- coding: utf-8 -*-

import json
from odoo import http, SUPERUSER_ID, _
from odoo.http import request, route
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.auth_signup.models.res_partner import SignupError
from odoo.addons.website.controllers.main import Website
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.exceptions import UserError

class AuthSignupHome(AuthSignupHome):

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        """
            After signing event, retirect to /my/activation page 
        """
        qcontext = self.get_auth_signup_qcontext()

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
                    user_sudo = request.env['res.users'].sudo().search([('login','=',qcontext.get('login'))], limit=1)

                #Send activation email to administrator
                admin_mail_template = request.env.ref('fmp-contact_activation.user_activation_mail_template_for_admin', raise_if_not_found=False)
                if admin_mail_template:
                    admin_mail_template.sudo().send_mail(request.env['res.users'].sudo().browse(SUPERUSER_ID).id, force_send=True)

                #Send activation email to new user
                user_mail_template = request.env.ref('fmp-contact_activation.user_activation_mail_template_for_new_user', raise_if_not_found=False)
                if user_mail_template:
                    user_mail_template.sudo().send_mail(user_sudo.id, force_send=True)

                user_sudo.sudo().write({'activation_state':'inactive'})

                #Redirect to /my/activation page
                return request.redirect('/my/activation')
            except UserError as e:
                qcontext['error'] = e.args[0]
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response        

    @http.route('/my/activation', type='http', auth='public', website=True, sitemap=False)
    def my_activation(self, *args, **kw):        
        """
            Redirect to this page
            while user is not being activated
        """
        return request.render('fmp-contact_activation.portal_my_activation', {})

class Website(Website):

    @http.route('/', type='http', auth="public", website=True, sitemap=True)
    def index(self, **kw):    
        related_partner_id = request.env['res.partner'].search([('email',"=",request.env.user.login)], limit=1)
        if related_partner_id and related_partner_id.activation_state=='inactive':
            return request.redirect('/my/activation')
        return super(Website, self).index(**kw) 

    @http.route('/check_user_activation', type='http', auth="public", website=True, sitemap=True)
    def check_user_activation(self, **kw):    
        related_partner_id = request.env['res.partner'].search([('email',"=",request.env.user.login)], limit=1)
        if related_partner_id and related_partner_id.activation_state=='inactive':
            return json.dumps({'user_status':'inactive'})
        return json.dumps({'user_status':'active'})

class CustomerPortal(CustomerPortal):

    @route(['/my', '/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        related_partner_id = request.env['res.partner'].search([('email',"=",request.env.user.login)], limit=1)
        if related_partner_id and related_partner_id.activation_state=='inactive':
            return request.redirect('/my/activation')
        return super(CustomerPortal, self).home(**kw)

class WebsiteSale(WebsiteSale):

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True, sitemap=WebsiteSale.sitemap_shop)
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        related_partner_id = request.env['res.partner'].search([('email',"=",request.env.user.login)], limit=1)
        if related_partner_id and related_partner_id.activation_state=='inactive':
            return request.redirect('/my/activation')
        public_user_id = request.env.ref('base.public_user')
        if request.env.user.id==public_user_id.id:
            return request.redirect('/web/login')
        return super(WebsiteSale, self).shop(page, category, search, min_price, max_price, ppg, **post)        

    @http.route(['/shop/cart'], type='http', auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):
        related_partner_id = request.env['res.partner'].search([('email',"=",request.env.user.login)], limit=1)
        if related_partner_id and related_partner_id.activation_state=='inactive':
            return request.redirect('/my/activation')
        public_user_id = request.env.ref('base.public_user')
        if request.env.user.id==public_user_id.id:
            return request.redirect('/web/login')
        return super(WebsiteSale, self).cart(access_token, revive, **post)        