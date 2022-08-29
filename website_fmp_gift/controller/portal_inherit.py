from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.http import request
from odoo import fields,http ,_
from collections import OrderedDict


class PortalGift(CustomerPortal):

    def _get_gifts_domain(self):
        partner = request.env.user.partner_id.id
        return [('expired_date','>=',fields.Date.today()),('partner_id','in',(False,partner)),('state','=','valid'),('balance','>', 0)]

    def _get_coupons_domain(self):
        website_id = request.website.id
        return [('website_id', 'in', [False, website_id]),('active','=',True)]


    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        gift_count = request.env['gift.card'].search(self._get_gifts_domain())
        values['gift_count'] = len(gift_count.filtered(lambda r: r.can_be_used()))
        values['coupon_count'] = len(request.env['coupon.program'].search(self._get_coupons_domain()).filtered(lambda r: not r._check_promo_code_portal(False, r.promo_code).get('error',False) ))
        return values


    @http.route(['/my/gifts', '/my/gifts/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_gifts(self, page=1,date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values={}
        domain = self._get_gifts_domain()
        GiftModel = request.env['gift.card']

        searchbar_sortings = {
            'date': {'label': _('Create Date'), 'order': 'create_date desc'},
            'expireddate': {'label': _('Expired Date'), 'order': 'expired_date desc'},
            'code': {'label': _('Code'), 'order': 'code desc'},
        }
        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},  }
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        gift_count = len(GiftModel.search(domain).filtered(lambda r: r.can_be_used()))
        # pager
        pager = portal_pager(
            url="/my/gifts",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=gift_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        gifts = GiftModel.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        gifts = gifts.filtered(lambda r: r.can_be_used())
        #request.session['my_invoices_history'] = invoices.ids[:100]

        values.update({
            'date': date_begin,
            'gifts': gifts,
            'page_name': 'gift',
            'pager': pager,
            'default_url': '/my/gifts',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return request.render("website_fmp_gift.portal_my_gift", values)

    @http.route(['/my/coupons', '/my/coupons/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_coupons(self, page=1,date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        values={}
        domain = self._get_coupons_domain()
        CouponModel = request.env['coupon.program']

        searchbar_sortings = {
            'date': {'label': _('Create Date'), 'order': 'create_date desc'},
            # 'expireddate': {'label': _('Expired Date'), 'order': 'expiration_date desc'},
            # 'code': {'label': _('Code'), 'order': 'code desc'},
        }
        # default sort by order
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},  }
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        coupon_count = len(CouponModel.search(domain).filtered(lambda r: not r._check_promo_code_portal(False, r.promo_code).get('error',False) ))
        # pager
        pager = portal_pager(
            url="/my/coupons",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=coupon_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        coupons = CouponModel.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        coupons = coupons.filtered(lambda r: not r._check_promo_code_portal(False, r.promo_code).get('error',False))
        #request.session['my_invoices_history'] = invoices.ids[:100]

        values.update({
            'date': date_begin,
            'coupons': coupons,
            'page_name': 'coupon',
            'pager': pager,
            'default_url': '/my/coupons',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return request.render("website_fmp_gift.portal_my_coupon", values)
