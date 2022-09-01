from odoo import models, fields,_ , api

class CrmTeamInherit(models.Model):
    _inherit = "crm.team"


    def _get_domain(self):
        return [('id', 'in', self.members_contact.ids)]

    members_contact = fields.One2many("res.partner",'team_id',string="Members (contact)")
    Responsables = fields.Many2many('res.partner', 'team_contact_rel', 'partner_id', 'team_id' ,domain=_get_domain)

