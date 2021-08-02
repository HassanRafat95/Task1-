from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    date_of_birth = fields.Date(related='partner_id.date_of_birth', string='Date of Birth')
    is_mature = fields.Boolean(related='partner_id.is_mature', string='Is Mature')


