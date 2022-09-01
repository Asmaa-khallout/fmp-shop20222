from odoo import models, fields,_ , api

class CrmTeamInherit(models.Model):
    _inherit = "crm.team"

    members_contact = fields.One2many("res.partner",'team_id',string="Members (contact)")
    Responsables = fields.Many2many('res.partner', 'team_contact_rel', 'partner_id', 'team_id')

    @api.onchange('Responsables')
    def Responsables_onchange(self):
        return {'domain': {'Responsables': [('id', 'in', self.members_contact.ids)]}}