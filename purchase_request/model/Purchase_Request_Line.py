from odoo import fields, models,api
from datetime import date, timedelta,datetime

class Purchase_Request_Line(models.Model):
    _name = "purchase.request.line"
    product_id = fields.Many2one('product.product')
    Description = fields.Char(string="Description", related="product_id.name")
    Quantity = fields.Float(default=1)
    cost_price = fields.Float(string="cost price" , related="product_id.standard_price", store=True)
    Total = fields.Float(compute="_compute_total", store=True)
    order_id = fields.Many2one("purchase.request")

    @api.depends("Quantity","cost_price")
    def _compute_total(self):
        for request_line in self:
            request_line.Total = request_line.Quantity * request_line.cost_price

    @api.onchange("Quantity","cost_price")
    def calc_Total(self):
        for request_line in self:
            request_line.Total = request_line.Quantity * request_line.cost_price



