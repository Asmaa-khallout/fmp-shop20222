from odoo import models, fields,_ , api
from datetime import datetime

class CrmLeadInherit(models.Model):
    _inherit = "crm.lead"

    @api.onchange('team_id')
    def user_domain_onchange(self):
        return {'domain': {'user_id': [('id', 'in', self.team_id.member_ids.ids)]}}

    state_flag = fields.Selection(selection=[('Plus','Plus'),('Moins','Moins')],default="Moins",strin='Statut de flagger')


    def flagger_lead(self):
        lead_ids = self.search([('type','=','opportunity'),('probability','<',0.4)])
        lead_ids.filtered(lambda r : (r.create_date- datetime.today()).days >15)
        lead_ids.write({'state_flag':'Plus'})
        return
