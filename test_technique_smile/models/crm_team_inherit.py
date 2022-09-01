from odoo import models, fields

class CrmTeamInherit(models.Model):
    _inherit = "crm.team"

    members_contact = fields.One2many("res.partner",'team_id',string="Members (contact)")