from odoo import fields, models,api
from datetime import date, timedelta,datetime


class PurchaseRequestLine(models.Model):
    _name = "purchase.request.line"
    product_id = fields.Many2one('product.product')
    description = fields.Char(string="Description", related="product_id.name")
    quantity = fields.Float(default=1)
    cost_price = fields.Float(string="cost price" , related="product_id.standard_price", store=True)
    total = fields.Float(compute="_compute_total", store=True)
    order_id = fields.Many2one("purchase.request")

    @api.onchange("quantity", "cost_price")
    @api.depends("quantity","cost_price")
    def _compute_total(self):
        for request_line in self:
            request_line.total = request_line.quantity * request_line.cost_price




