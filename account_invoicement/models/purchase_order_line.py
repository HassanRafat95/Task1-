from odoo import fields, models,api

class PurchaseOrderLine(models.Model):
    _inherit = ['purchase.order.line']

    sub_total_after_discount = fields.Float("sub total after discount ", compute="_compute_total_after_discount" , store=True)

    @api.onchange("product_qty", "price_unit")
    @api.depends("product_qty","price_unit")
    def _compute_total_after_discount(self):
        print("------------------------------------------------------------")
        for order_line in self:
            print("------------------------------------------------------------")
            order_line.sub_total_after_discount = (order_line.product_qty * order_line.price_unit) * ((100 - order_line.order_id.discount)/100)
            print("------------------------------------------------------------")
            print(order_line.product_id)
            print(order_line.sub_total_after_discount)
