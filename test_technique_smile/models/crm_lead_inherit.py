from odoo import models, fields,_ , api

class CrmLeadInherit(models.Model):
    _inherit = "crm.lead"

    @api.model
    def _get_user_domain(self):
        return [('id', 'in', self.team_id.member_ids.ids)]


    user_id = fields.Many2one('res.users', domain=_get_user_domain)
