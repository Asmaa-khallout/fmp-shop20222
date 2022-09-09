# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.osv.expression import AND, OR, FALSE_DOMAIN
from odoo.tools import escape_psql, pycompat
import logging

_logger = logging.getLogger(__name__)
class WebsiteInherit(models.Model):
    _inherit = 'website'

    def _search_exact(self, search_details, search, limit, order):
        """
        Performs a search with a search text

        :param search_details: see :meth:`_search_get_details`
        :param search: text against which to match results
        :param limit: maximum number of results per model type involved in the result
        :param order: order on which to sort results within a model type

        :return: tuple containing:
            - total number of results across all involved models
            - list of results per model made of:
                - initial search_detail for the model
                - count: number of results for the model
                - results: model list equivalent to a `model.search()`
        """
        all_results = []
        total_count = 0
        _logger.info("seaarch details")
        _logger.info("search details %s " %(search_details))
        _logger.info("search : %s" %(search))
        for search_detail in search_details:
            model = self.env[search_detail['model']]
            if(search_detail['model']=="product.template"):
                results, count = model._search_fetch_custom(search_detail, search, limit, order)
            else:
                results, count = model._search_fetch(search_detail, search, limit, order)
            search_detail['results'] = results
            total_count += count
            search_detail['count'] = count
            all_results.append(search_detail)
        return total_count, all_results



class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    # def _search_build_domain_custom(self, domain, search, fields, extra=None):
    #     """
    #     Builds a search domain AND-combining a base domain with partial matches of each term in
    #     the search expression in any of the fields.
    #
    #     :param domain: base domain combined in the search expression
    #     :param search: search expression string
    #     :param fields: list of field names to match the terms of the search expression with
    #     :param extra: function that returns an additional subdomain for a search term
    #
    #     :return: domain limited to the matches of the search expression
    #     """
    #     domains = domain.copy()
    #     _logger.info("domain asmmaaa")
    #     _logger.info(fields)
    #     if search:
    #         for search_term in search.split(' '):
    #             subdomains = []
    #             for field in fields:
    #                 subdomains.append([(field, 'ilike', escape_psql(search_term))])
    #             if extra:
    #                 subdomains.append(extra(self.env, search_term))
    #             domains.append(OR(subdomains))
    #     return AND(domains)

    def _search_build_domain_custom(self, domain, search, fields, extra=None):
        """
        Builds a search domain AND-combining a base domain with partial matches of each term in
        the search expression in any of the fields.

        :param domain: base domain combined in the search expression
        :param search: search expression string
        :param fields: list of field names to match the terms of the search expression with
        :param extra: function that returns an additional subdomain for a search term

        :return: domain limited to the matches of the search expression
        """
        domains = domain.copy()
        _logger.info("domain asmmaaa ")
        _logger.info(fields)
        _logger.info("domains copy %s" %(domains))
        subdomains = []
        if search:
            for field in fields:
                if(field !="product_variant_ids.default_code"):
                    for search_term in search.split(' '):
                        subdomains = []
                        subdomains.append([(field, 'ilike', escape_psql(search_term))])
                        if extra:
                            subdomains.append(extra(self.env, search_term))
                        domains.append(OR(subdomains))
                else:
                    subdomains.append([(field, '=', escape_psql(search))])
                    domains.append(OR([(field, '=', escape_psql(search))]))

        return AND(domains)



    @api.model
    def _search_fetch_custom(self, search_detail, search, limit, order):
        _logger.info("asmaa tu es laa !!!")

        fields = search_detail['search_fields']
        base_domain = search_detail['base_domain']
        domain = self._search_build_domain_custom(base_domain, search, fields, search_detail.get('search_extra'))
        _logger.info("dommain est %s" %(domain))
        model = self.sudo() if search_detail.get('requires_sudo') else self
        results = model.search(
            domain,
            limit=limit,
            order=search_detail.get('order', order)
        )
        count = model.search_count(domain)
        return results, count

    @api.model
    def _search_get_detail(self, website, order, options):
        with_image = options['displayImage']
        with_description = options['displayDescription']
        with_category = options['displayExtraLink']
        with_price = options['displayDetail']
        domains = [website.sale_product_domain()]
        category = options.get('category')
        min_price = options.get('min_price')
        max_price = options.get('max_price')
        attrib_values = options.get('attrib_values')
        if category:
            domains.append([('public_categ_ids', 'child_of', unslug(category)[1])])
        if min_price:
            domains.append([('list_price', '>=', min_price)])
        if max_price:
            domains.append([('list_price', '<=', max_price)])
        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domains.append([('attribute_line_ids.value_ids', 'in', ids)])
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domains.append([('attribute_line_ids.value_ids', 'in', ids)])
        search_fields = ['name', 'product_variant_ids.default_code']
        fetch_fields = ['id', 'name', 'website_url']
        mapping = {
            'name': {'name': 'name', 'type': 'text', 'match': True},
            'product_variant_ids.default_code': {'name': 'product_variant_ids.default_code', 'type': 'text',
                                                 'match': True},
            'website_url': {'name': 'website_url', 'type': 'text', 'truncate': False},
        }
        if with_image:
            mapping['image_url'] = {'name': 'image_url', 'type': 'html'}
        if with_description:
            # Internal note is not part of the rendering.
            search_fields.append('description')
            fetch_fields.append('description')
            search_fields.append('description_sale')
            fetch_fields.append('description_sale')
            mapping['description'] = {'name': 'description_sale', 'type': 'text', 'match': True}
        if with_price:
            mapping['detail'] = {'name': 'price', 'type': 'html', 'display_currency': options['display_currency']}
            mapping['detail_strike'] = {'name': 'list_price', 'type': 'html',
                                        'display_currency': options['display_currency']}
        if with_category:
            mapping['extra_link'] = {'name': 'category', 'type': 'dict', 'item_type': 'text'}
            mapping['extra_link_url'] = {'name': 'category_url', 'type': 'dict', 'item_type': 'text'}
        return {
            'model': 'product.template',
            'base_domain': domains,
            'search_fields': search_fields,
            'fetch_fields': fetch_fields,
            'mapping': mapping,
            'icon': 'fa-shopping-cart',
        }