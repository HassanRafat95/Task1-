from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _name = "purchase.order"
    _inherit = ['purchase.order']
    _description = "Purchase Order"
    purchase_request_id = fields.fields.Many2one("purchase.request")

