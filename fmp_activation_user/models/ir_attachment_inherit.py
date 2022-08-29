# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError


class IrAttachmentInherit(models.Model):
    _inherit = 'ir.attachment'

    file_activation =  fields.Boolean("File activation")