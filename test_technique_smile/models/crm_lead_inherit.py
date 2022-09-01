from odoo import models, fields,_ , api

class CrmLeadInherit(models.Model):
    _inherit = "crm.lead"


    @api.depends('team_id')
    def Responsables_onchange(self):
        return {'domain': {'user_id': [('id', 'in', self.team_id.member_ids.ids)]}}