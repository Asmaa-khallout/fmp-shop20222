from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import  Website
from odoo.addons.website_sale.controllers.main import WebsiteSale


class CustomWebsiteSale(http.Controller):

    @http.route(['/terms-of-sales'], type='http', auth='public', website=True, sitemap=False)
    def notice(self, **post):
        return request.render('fmp_france_custom_website.terms_sales_template')

    @http.route(['/mentions-legales'], type='http', auth='public', website=True, sitemap=False)
    def faq(self, **post):
        return request.render('fmp_france_custom_website.mentions_legales_template')

    @http.route(['/rgpd'], type='http', auth='public', website=True, sitemap=False)
    def get_echanges(self, **post):
        return request.render('fmp_france_custom_website.rgpd_template')

class ThemeWebsiteInherit(Website):

    @http.route('/website/dr_search', type='json', auth="public", website=True)
    def dr_search(self, term, max_nb_chars, options, **kw):
        result =  super(ThemeWebsiteInherit,self).dr_search(term=term,max_nb_chars=max_nb_chars,options=options,**kw)
        result['activation']=request.env.user.partner_id.activation_state
        return result

class ThemePrimeWebsiteSaleInherit(WebsiteSale):
    @http.route('/theme_prime/get_products_data', type='json', auth='public', website=True)
    def get_products_data(self, domain, fields=[], options={}, limit=25, order=None, **kwargs):
        result = super(ThemePrimeWebsiteSaleInherit,self).get_products_data(domain=domain,fields=fields,options=options,limit=limit,order=order,**kwargs)
        result['activation'] = request.env.user.partner_id.activation_state
        return result
