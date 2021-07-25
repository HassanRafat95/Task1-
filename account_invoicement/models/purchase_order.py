from odoo import fields, models,api, _

class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']
    total_discount = fields.Float(compute="_compute_total")
    primary_total = fields.Float(compute="_compute_total")

    @api.depends("order_line.product_qty","order_line.price_unit","order_line.discount")
    def _compute_total(self):
        for record in self:
            record.primary_total = sum((l.product_qty * l.price_unit)for l in record.order_line)
            record.total_discount = sum((l.product_qty * l.price_unit * (l.discount /100 ))for l in record.order_line)



