from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    allowed_discount_account_id = fields.Many2one("account.account", required=True)
    allowed_discount_product_id = fields.Many2one("product.product", required=True, domain=[('type', '=', 'service')])
