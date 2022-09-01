from odoo import models, fields,_ , api
from datetime import datetime

class CrmLeadInherit(models.Model):
    _inherit = "crm.lead"

    @api.model
    def _get_user_domain(self):
        return [('id', 'in', self.team_id.member_ids.ids)]


    user_id = fields.Many2one('res.users', domain=_get_user_domain)
    state_flag = fields.Selection(selection=[('Plus','Plus'),('Moins','Moins')],default="Moins",strin='Statut de flagger')


    def flagger_lead(self):
        lead_ids = self.search([('type','opportunity'),('probability','<',0.4)])
        lead_ids.filterd(lambda r : (r.create_date- datetime.today()).days >15)
        lead_ids.write({'state_flag':'Plus'})
        return
