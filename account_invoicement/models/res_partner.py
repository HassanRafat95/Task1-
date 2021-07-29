from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    invoices_total = fields.Float(string="Invoices Total", default=0, readonly=True)
