from odoo import api, models, fields
from odoo.tools.translate import _


class Partner(models.Model):
    _inherit = 'res.partner'
    invoices_total = fields.Float(string="Invoices Total",default=0)
