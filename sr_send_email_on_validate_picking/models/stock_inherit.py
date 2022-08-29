# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import xlwt
import io
import base64


class respartner(models.Model):
    _inherit = 'res.partner'

    def _default_confirmation_mail_template_customer(self):
        try:
            return self.env.ref(
                'sr_send_email_on_validate_picking.mail_template_data_delivery_confirmation_for_partner').id
        except ValueError:
            return False

    opt_in_email_excel = fields.Boolean('Opt In for Send Email with Excel Attachment')
    email_template_id = fields.Many2one('mail.template', string="Email Template confirmation picking",
                                        domain="[('model', '=', 'stock.picking')]",
                                        default=_default_confirmation_mail_template_customer,
                                        help="Email sent to the customer once the order is done.")


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _get_customer_product_code(self):
        partner_id = self.partner_id.id if not self.partner_id.parent_id else self.partner_id.parent_id.id
        customer_ids = self.env['product.customer.info'].search(
            [('product_id', '=', self.product_id.id), ('partner_id', '=', partner_id)])
        if customer_ids:
            return customer_ids[0].customer_product_code
        else:
            return '-'

    def _get_customer_product_name(self):
        partner_id = self.partner_id.id if not self.partner_id.parent_id else self.partner_id.parent_id.id
        customer_ids = self.env['product.customer.info'].search(
            [('product_id', '=', self.product_id.id), ('partner_id', '=', partner_id)])
        if customer_ids:
            return customer_ids[0].customer_product_name
        else:
            return '-'


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    need_to_send_email = fields.Boolean('Need to send Email')

    def action_resend_email(self):
        if self.partner_id.opt_in_email_excel:
            filename = 'TimeSheet_Data.xls'
            workbook = xlwt.Workbook()
            worksheet = workbook.add_sheet('Sheet 1')

            worksheet.write(0, 0, 'Code Client')
            worksheet.write(0, 1, 'Code FMP (Internal Id)')
            worksheet.write(0, 2, 'Name (Internal)')
            worksheet.write(0, 3, 'Quantité')
            worksheet.write(0, 4, 'Prix unitaire HT')
            row = 2
            col = 0
            for line in self.move_ids_without_package:
                partner_id = self.partner_id.id if not self.partner_id.parent_id else self.partner_id.parent_id.id
                customer_ids = self.env['product.customer.info'].search(
                    [('product_id', '=', line.product_id.id), ('partner_id', '=', partner_id)])
                if customer_ids:
                    client_code = customer_ids[0].customer_product_code
                else:
                    client_code = '-'
                price = 0
                if line.sale_line_id:
                    price = line.sale_line_id.price_unit
                elif line.purchase_line_id:
                    price = line.purchase_line_id.price_unit
                worksheet.write(row, col, client_code)
                worksheet.write(row, col + 1, line.product_id.default_code)
                worksheet.write(row, col + 2, line.product_id.name)
                worksheet.write(row, col + 3, line.quantity_done)
                worksheet.write(row, col + 4, price)
                row += 1

            fp = io.BytesIO()
            workbook.save(fp)

            data1 = base64.encodestring(fp.getvalue())
            attachment_obj = self.env['ir.attachment']
            final_att = []
            attachment = attachment_obj.sudo().create({'name': self.name + ".xls",
                                                       'type': 'binary',
                                                       'mimetype': 'application/vnd.ms-excel',
                                                       'res_id': self.id,
                                                       'res_model': 'stock.picking',
                                                       'datas': data1})
            final_att.append(attachment.id)
            email_template_obj = self.env['mail.template'].browse(self.partner_id.email_template_id.id)
            values = email_template_obj.generate_email(self.id)
            pdf_attachment_id = attachment_obj.sudo().create({
                'name': values['attachments'][0][0],
                #                 'datas_fname': values['attachments'][0][0],
                'datas': values['attachments'][0][1],
                'res_id': self.id,
                'res_model': 'stock.picking',
            })
            final_att.append(pdf_attachment_id.id)
            values['email_from'] = self.env['res.users'].browse(self._uid).partner_id.email
            values['email_to'] = self.partner_id.email
            #         values['res_id'] = self.id
            values['attachment_ids'] = [(6, 0, final_att)]
            #         values['author_id'] = self.env['res.users'].browse(self._uid).partner_id.id
            #         values['body_html'] = """Bonjour,
            # Veuillez trouver ci-joint le détail de votre expédition ce jour.
            # Colis envoyé par [SHIPPING METHOD] avec le numéro de suivi """
            mail_mail_obj = self.env['mail.mail']
            del values['attachments']
            msg_id = mail_mail_obj.sudo().create(values)
            if msg_id:
                mail_mail_obj.send([msg_id])
                msg_id.send()

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        self.need_to_send_email = True
        return res

    def send_auto_email_to_customer(self):
        picking = self.search([('need_to_send_email', '=', True)])
        print("========picking", picking)
        for record in picking:
            if record.partner_id.opt_in_email_excel:
                record.action_resend_email()
                record.need_to_send_email = False
        return True
