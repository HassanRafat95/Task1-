from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    allowed_discount_account_id = fields.Many2one(related='company_id.allowed_discount_account_id', required=True,
                                        readonly=False)
    allowed_discount_product_id = fields.Many2one(related='company_id.allowed_discount_product_id', required=True,
                                                  readonly=False)
