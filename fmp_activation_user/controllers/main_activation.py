# -*- coding: utf-8 -*-
import logging

from odoo.exceptions import UserError
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request,route
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http

_logger = logging.getLogger(__name__)

class AuthActivation(CustomerPortal):
    @route('/my/activation', type='http', auth='user', website=True, sitemap=False)
    def my_activation(self, *args, **kw):
        related_partner_id = request.env.user.partner_id
        if related_partner_id and related_partner_id.activation_state == 'inactive':
            return request.render('fmp_activation_user.portal_my_activation', {})
        return request.redirect('/')


    # @http.route('/', type='http', auth="public", website=True, sitemap=True)
    # def index(self, **kw):
    #     related_partner_id = request.env.user.partner_id
    #     _logger.info("indeeeeex %s " %(related_partner_id))
    #     if related_partner_id and related_partner_id.activation_state == 'inactive':
    #         return request.redirect('/my/activation')
    #     return super(AuthActivation, self).index(**kw)


    @route(['/my','/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        related_partner_id = request.env.user.partner_id
        if related_partner_id and related_partner_id.activation_state == 'inactive':
            return request.redirect('/my/activation')
        return super(AuthActivation, self).home(**kw)


class ActivationWebsiteSale(WebsiteSale):

    @http.route(['/shop/cart'], type='http', auth="user", website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):
        related_partner_id = request.env.user.partner_id
        if related_partner_id and related_partner_id.activation_state=='inactive':
            return request.redirect('/my/activation')
        return super(ActivationWebsiteSale, self).cart(access_token, revive, **post)
