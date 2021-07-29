from odoo import fields, models


class PickingType(models.Model):
    _inherit = "stock.picking.type"
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
