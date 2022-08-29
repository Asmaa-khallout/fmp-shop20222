# -*- coding: utf-8 -*-
{
  "name"                 :  "Website Coupons & Gifts",
  "summary"              :  """The module allows display coupons and vouchers for Odoo website. The voucher code can be used by the customer to obtain discount on orders.""",
  "category"             :  "Website",
  "version"              :  "15.1.0",
  "sequence"             :  1,
  "author"               :  "KHALLOUT Asmaa",
  "description"          :  "Odoo Website Coupons & Vouchers",
  'depends'              : ['website','website_sale_gift_card'],
  "data"                 :  [
                             'views/templates.xml',
                             'views/portal_home_gift.xml',
                             'security/ir.model.access.csv',
                            ],
  "assets"               : {'web.assets_frontend': ["/website_fmp_gift/static/src/js/voucher.js","/website_fmp_gift/static/src/css/voucher.css"]},
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
}
