from odoo import models, fields,_ , api

class CrmLeadInherit(models.Model):
    _inherit = "crm.lead"


    @api.onchange('user_id')
    def Responsables_onchange(self):
        return {'domain': {'user_id': [('team_id', '=', self.team)]}}