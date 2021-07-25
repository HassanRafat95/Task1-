from odoo import fields, models,api

class PurchaseOrderLine(models.Model):
    _inherit = ['purchase.order.line']

    sub_total_after_discount = fields.Float("sub total after discount ", compute="_compute_total_after_discount" , store=True)

    @api.onchange("product_qty", "price_unit","order_id.discount")
    @api.depends("product_qty","price_unit","order_id.discount")
    def _compute_total_after_discount(self):
        for order_line in self:
            order_line.sub_total_after_discount = (order_line.product_qty * order_line.price_unit) * ((100 - order_line.order_id.discount)/100)
