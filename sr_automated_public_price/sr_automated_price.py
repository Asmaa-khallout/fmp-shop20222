from odoo import api, fields, models, _
from odoo.exceptions import Warning
from odoo.exceptions import UserError, ValidationError


class srSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def product_id_change(self):
        res = super(srSaleOrderLine, self).product_id_change()
        if self.product_id.price_category:
            cost_price = self.product_id.standard_price
            if self.product_id.price_category.public_price_list_id.id == self.order_id.pricelist_id.id:
                percentage = 1 - (self.product_id.public_price_list_margin / 100)
            elif self.product_id.price_category.distributor_price_list_id.id == self.order_id.pricelist_id.id:
                percentage = 1 - (self.product_id.distributor_price_list_margin / 100)
            else:
                percentage = 1
            self.write({'price_unit': cost_price / percentage})
        return res

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        res = super(srSaleOrderLine, self).product_uom_change()
        print("===new=====res", res)
        if self.product_id.price_category:
            cost_price = self.product_id.standard_price
            if self.product_id.price_category.public_price_list_id.id == self.order_id.pricelist_id.id:
                percentage = 1 - (self.product_id.public_price_list_margin / 100)
            elif self.product_id.price_category.distributor_price_list_id.id == self.order_id.pricelist_id.id:
                percentage = 1 - (self.product_id.distributor_price_list_margin / 100)
            else:
                percentage = 1
            print("==new======percentage", percentage, cost_price / percentage)
            self.write({'price_unit': cost_price / percentage})
        return res


class srProductProduct(models.Model):
    _inherit = 'product.product'

    distributor_price = fields.Float('Distributor Price')
    price_category = fields.Many2one('sr.price.category', string="Price Category")
    public_price_list_margin = fields.Float(related='price_category.public_price_list_margin', string="Public Margin")
    distributor_price_list_margin = fields.Float(related='price_category.distributor_price_list_margin', string="Distributor Margin")

    def set_auto_set_price(self):
        products = self.search([])
        for product in products:
            if product.price_category:
                cost_price = product.standard_price
                percentage = 1 - (product.public_price_list_margin / 100)
                product.write({'lst_price': cost_price / percentage})
        sync_id = self.env['synchronization.wizard'].create({'instance_id': self.env['connector.instance'].search([], limit=1).id,'action': 'update'})
        sync_id.with_context(check=False, active_model='connector.snippet', active_id=sync_id.id, active_ids=sync_id.ids).start_product_synchronization()
        return

    def write(self, vals):
        print("========vals", vals)
        res = super(srProductProduct, self).write(vals)
        if vals.get('standard_price'):
            if self.price_category:
                percentage = 1 - (self.public_price_list_margin / 100)
                dist_percentage = 1 - (self.distributor_price_list_margin / 100)
                self.lst_price = self.standard_price / percentage
                self.distributor_price = self.standard_price / dist_percentage
        return res


class srPriceCategory(models.Model):
    _name = 'sr.price.category'

    def _get_default_public_price_lit(self):
        public_price_list_id = self.env['product.pricelist'].search([('currency_id.name', '=', 'EUR')])
        if public_price_list_id:
            return public_price_list_id[0].id

    def _get_default_distributor_price_lit(self):
        distributor_price_list_id = self.env['product.pricelist'].search(
            [('currency_id.name', '=', 'EUR'), ('name', 'ilike', 'Distributor')])
        if distributor_price_list_id:
            return distributor_price_list_id[0].id

    name = fields.Char('Name', required=True)
    public_price_list_id = fields.Many2one('product.pricelist', name="Public Price List", required=True, domain=[('currency_id.name', '=', 'EUR')], default=_get_default_public_price_lit)
    public_price_list_margin = fields.Float('Public Margin (%)', required=True)
    distributor_price_list_id = fields.Many2one('product.pricelist', name="Distributor Price List", required=True, domain=[('currency_id.name', '=', 'EUR'), ('name', 'ilike', 'Distributor')], default=_get_default_distributor_price_lit)
    distributor_price_list_margin = fields.Float('Distributor Margin (%)', required=True)
    product_ids = fields.Many2many('product.product', string="Products")

    @api.model
    def create(self, vals):
        res = super(srPriceCategory, self).create(vals)
        for product in res.product_ids:
            cost_price = product.standard_price
            percentage = 1 - (res.public_price_list_margin / 100)
            dist_percentage = 1 - (res.distributor_price_list_margin / 100)
            product.write({'lst_price': cost_price / percentage,
                           'price_category': res.id,
                           'distributor_price': cost_price / dist_percentage})
        return res

    def write(self, vals):
        if vals.get('product_ids'):
            old_list = self.product_ids.ids
            new_list = vals.get('product_ids')[0][2]
            new_old_product = list(set(old_list) ^ set(new_list))
            for product in new_old_product:
                if self.env['product.product'].browse(product).price_category:
                    self.env['product.product'].browse(product).price_category = False
                else:
                    product_brw = self.env['product.product'].browse(product)
                    cost_price = product_brw.standard_price
                    percentage = 1 - (self.public_price_list_margin / 100)
                    dist_percentage = 1 - (self.distributor_price_list_margin / 100)
                    product_brw.write({'lst_price': cost_price / percentage,
                                       'price_category': self.id,
                                       'distributor_price': cost_price / dist_percentage})

        return super(srPriceCategory, self).write(vals)
