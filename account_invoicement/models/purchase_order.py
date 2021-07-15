from odoo import fields, models,api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']
    discount = fields.Float(default=0)
    total_after_discount = fields.Float(compute="_compute_total",store=True)

    @api.onchange("discount")
    def _check_discount(self):
        for record in self:
            if record.discount < 0:
                record.discount = 0
                raise UserError(_("Discount can not less than zero"))
            else:
                if record.discount > 100:
                    record.discount = 100
                    raise UserError(_("Discount can not more than 100"))


    @api.depends("order_line.sub_total_after_discount")
    def _compute_total(self):
        for record in self:
            record.total_price = sum(l.sub_total_after_discount for l in record.order_line)



