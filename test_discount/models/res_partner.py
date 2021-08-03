from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    allowed_discount = fields.Float("allowed discount")
