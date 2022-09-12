# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import logging
import pandas as pd
from PIL import Image,ImageColor
import urllib.request, ssl, base64
from .prestapi import PrestaShopWebServiceDict

_logger = logging.getLogger(__name__)


class setting_setting_amb(models.TransientModel):
    _name = 'setting.setting'
    _description = 'Setting'

    url_upload = fields.Char("Url")




    def _prestashop_get_product_images_vals(self,prestashop, media):
        vals = dict()
        message = ''
        data = None
        image_url = media
        if image_url:
            prestashop = prestashop
            data = prestashop.get(image_url)
            image_data = base64.b64encode(data)
            vals['image'] = image_data
            return vals
        return {'image':False}

    def _get_default_image(self, prestashop, product_id, default_image_id):
        image_data = 'images/products/%s/%s'%(product_id, default_image_id)
        _logger.info("image date 1 %s" %(image_data))
        image_data = self._prestashop_get_product_images_vals(prestashop,image_data)
        image_data = image_data.get("image")
        if not image_data:
            return False
        return image_data

    def get_images_products(self):
        products = self.env['product.template'].sudo().search([('x_id_presta','!=',False)])
        prestashop = PrestaShopWebServiceDict(
            "https://dev.fmp-france.com/", "1IGIJ887GZUZBACQYTSJRVFI2IFDGW48")
        count=0
        for record in products:
            _logger.info("product %s "%(record))
            record.product_template_image_ids.unlink()
            image_1920 = False
            liste_image_a = []
            try:
                product = prestashop.get("products", str(record.x_id_presta))
                product = product.get('product')
                # images = product.get('image')
                default_image_id = product.get("id_default_image").get('value')
                image_id_remote = product['associations']['images']

                if 'image' in image_id_remote:
                    image_id_list = product['associations']['images']['image']
                    if (type(image_id_list) is dict):
                        data_par = [v for k, v in image_id_list.items()]
                    else:
                        data_par = [v['id'] for v in image_id_list]
                    _logger.info("data par  %s " % (data_par))
                    for v in data_par:
                        if (default_image_id == v):
                            image_data = self._get_default_image(prestashop, product['id'], v)
                            image_1920 = image_data
                        else:
                            image_data = self._get_default_image(prestashop, product['id'], v)
                            i_record = self.env['product.image'].create({'name': record.name, 'image_1920': image_data})
                            liste_image_a.append((4, i_record.id))
                record.write({'image_1920': image_1920, 'product_template_image_ids': liste_image_a})
            except Exception as e :
                _logger.info("erreur ici %s %s " %(record,e))
                count +=1
                record.write({'image_1920': image_1920, 'product_template_image_ids': liste_image_a})
                continue

        _logger.info("count erreur %s "%(count))
        _logger.info("fin")





    def publier_product(self):
        products = self.env['product.template'].sudo().search([])
        prestashop = PrestaShopWebServiceDict(
            "https://dev.fmp-france.com/", "1IGIJ887GZUZBACQYTSJRVFI2IFDGW48")
        count=0
        for record in products:
            try :
                is_published = False
                if (record.x_id_presta):
                    product = prestashop.get("products", str(record.x_id_presta))
                    product = product.get('product')
                    actif = product['active']
                    if (actif == '1'):
                        is_published = True
                record.is_published = is_published
            except:
                count +=1
                _logger.info("erreur ici %s" % (record))
                record.is_published = False
                continue
        _logger.info("count erreur %s "%(count))




        return True

    def activate_category_website(self):
        df = pd.read_excel("/mnt/extra-addons/custom_setting/models/pc.xlsx")
        for i, row in df.iterrows():
            a = row.to_dict()
            id_category=a['id_category']
            active = a['active']
            if (str(id_category) not in ("nan", "/", "")):
                cat = self.env['product.public.category'].search([('active','in',(True,False)),('seo_name','=',str(id_category))])
                cat.write({'active':True if active == 1 else False})
            else:
                _logger("not found %s " %(a))
        _logger.info("fiin")

    def create_cat(self):
        df = pd.read_excel("/home/odoo/src/user/custom_setting/models/ps-samedi.xlsx")
        for i, row in df.iterrows():
            a = row.to_dict()
            id_category=a['id_category']
            active = a['active']
            name= a['name']
            if (str(id_category) not in ("nan", "/", "")):
                cat = self.env['product.public.category'].search([('seo_name','=',str(id_category)),('active','in',(True,False))])
                if(not cat):
                    data ={'name':name,'website_description':a['description'] if str(a['description']) not in ("nan", "/", "") else False, 'seo_name':str(id_category)}
                    self.env['product.public.category'].create(data)
    def create_parent(self):
        df = pd.read_excel("/home/odoo/src/user/custom_setting/models/ps-samedi.xlsx")
        for i, row in df.iterrows():
            a = row.to_dict()
            id_parent=a['id_parent']
            id_category = a['id_category']
            if (str(id_parent) not in ("nan", "/", "")):
                cat = self.env['product.public.category'].search([('seo_name', '=', str(id_category)),('active','in',(True,False))])
                cat_parent = self.env['product.public.category'].search([('seo_name','=',str(id_parent)),('active','in',(True,False))])
                if(cat and cat_parent):
                    cat.write({'parent_id': cat_parent.id})
                else:
                    _logger.info("erreur %s de ligne %s" %(a,i))
            else:
                _logger.info("naaan %s %s" %(id_category,id_parent))

    def insert_mapping_product(self):
        df = pd.read_excel("/home/odoo/src/user/custom_setting/models/ps_category_product_samedi.xlsx")
        for i, row in df.iterrows():
            a = row.to_dict()
            id_category = a['id_category']
            id_product = a['id_product']
            if (str(id_product) not in ("nan", "/", "")):
                cat = self.env['product.public.category'].search([('seo_name', '=', str(id_category)),('active','in',(True,False))])
                product = self.env['product.template'].search([('x_id_presta','=',id_product),('active','in',(True,False))])
                if(cat and product):
                    product.public_categ_ids=[(4,cat.id)]
                else:
                    _logger.info("non trouvee %s ligne %s" %(a,i))
            else:
                _logger.info("errreur (2) %s ligne %s" %(a,i))



        _logger.info("fiiiiiiiiiiiiiiiiiiiiiiiin")


    def create_portal_contact(self):
        df = pd.read_excel("/home/odoo/src/user/custom_setting/models/liste des clients a activer.xlsx")
        partner_env = self.env['res.partner']
        count=0
        file = open("/home/odoo/src/user/custom_setting/models/get_exception.txt", "w")
        for i, row in df.iterrows():
            dict = row.to_dict()
            partner_id = dict['Référence commande']
            term = partner_id
            if('(' in term):
                term = partner_id.split('(')[0]
            if ("," in term):
                term = term.split(",")[0]
            if(']' in term):
                term = term.split(']')[1]
            a= partner_env.search([('display_name', '=', term.strip())])

            _logger.info("le client est %s display :%s" %(a,term.strip()))
            if(len(a)!=1):
                count +=1
            if(a):
                if (a.parent_id):
                    a = a.parent_id
                if (len(a) == 1):
                    try:
                        company = a.company_id or self.env.company
                        _logger.info("aa " % (a))
                        user = self.env['res.users'].with_context(no_reset_password=True)._create_user_from_template({
                            'name': a.name.split(']')[1],
                            'login': a.email,
                            'partner_id': a.id,
                            'company_id': self.env.company.id,
                            'company_ids': [(6, 0, self.env.company.ids)],
                        })
                        user.sudo().partner_id.activation_state = "active"
                        # user.action_reset_password()
                    except Exception as e:
                        _logger.info(e)
                        _logger.info(dict)
                        file.write("---------------------------Exception  ------------------- : %s \n" % (dict))
                        file.write(("\n----------------------\n"))
                        continue
                else:
                    _logger.info(" a <>1 %s" % (term))
                    file.write("---------------------------ELse %s  ------------------- : %s \n" % (len(a), dict))
                    file.write(("\n----------------------\n"))


        file.close()
        _logger.info("count %s" %(count))











