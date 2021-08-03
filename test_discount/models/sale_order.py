from odoo import models, api, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    discount_account_id = fields.Many2one(related='company_id.allowed_discount_account_id')
    discount_product_id = fields.Many2one(related='company_id.allowed_discount_product_id')

    @api.onchange('partner_id')
    def check_customer_discount(self):
        for rec in self:
            if rec.name != 'New':
                if rec.partner_id.allowed_discount > 0:
                    check_product = False
                    for line in rec.order_line:
                        if line.product_id == rec.discount_product_id.id:
                            check_product = True
                            if line.price_unit != (
                                    rec.discount_product_id.list_price - rec.partner_id.allowed_discount):
                                line.price_unit = rec.discount_product_id.list_price - rec.partner_id.allowed_discount

                    if not check_product:
                        vals = {
                            'product_id': rec.discount_product_id.id,
                            'price_unit': rec.discount_product_id.list_price - rec.partner_id.allowed_discount,
                            'product_uom_qty': 1,
                            'order_id': rec.id
                        }
                        order_line = self.env['sale.order.line'].create(vals)

    @api.model
    def create(self, vals):
        result = super(SaleOrder, self).create(vals)
        if result.partner_id.allowed_discount > 0:
            line_vals = {
                'product_id': result.discount_product_id.id,
                'price_unit': result.discount_product_id.list_price - result.partner_id.allowed_discount,
                'product_uom_qty': 1,
                'order_id': result.id
            }
            order_line = self.env['sale.order.line'].create(line_vals)
        return result


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        result = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        if self.order_id.partner_id.allowed_discount > 0 and self.product_id.id == self.order_id.discount_product_id.id:
            result['account_id'] = self.order_id.discount_account_id.id
        return result
