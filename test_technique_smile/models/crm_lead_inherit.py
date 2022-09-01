from odoo import models, fields,_ , api

class CrmLeadInherit(models.Model):
    _inherit = "crm.lead"
    user_id =  fields.Many2one('res.users' ,domain=lambda self: self._get_user_domain())


    @api.onchange('user_id')
    def _get_user_domain(self):
        return [('id', 'in', self.team_id.member_ids.ids)]