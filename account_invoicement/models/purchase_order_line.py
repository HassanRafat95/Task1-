from odoo import fields, models,api

class PurchaseOrderLine(models.Model):
    _inherit = ['purchase.order.line']

    discount = fields.Float()

    @api.onchange("discount")
    def _check_discount(self):
        for record in self:
            if record.discount < 0:
                record.discount = 0
            else:
                if record.discount > 100:
                    record.discount = 100

    @api.depends('product_qty', 'price_unit', 'taxes_id','discount')
    def _compute_amount(self):
        for line in self:
            vals = line._prepare_compute_all_values()
            vals['price_unit'] = vals['price_unit']*((100-line.discount)/100)
            taxes = line.taxes_id.compute_all(
                vals['price_unit'],
                vals['currency_id'],
                vals['product_qty'],
                vals['product'],
                vals['partner'])
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })



    def _prepare_account_move_line(self, move=False):
        res = super(PurchaseOrderLine,self)._prepare_account_move_line()
        res['discount'] = self.discount
        if self.order_id.picking_type_id.analytic_account_id:
            res['analytic_account_id'] = self.order_id.picking_type_id.analytic_account_id.id
        return res

    @api.depends('product_id', 'date_order')
    def _compute_analytic_id_and_tag_ids(self):
        for rec in self:
            super(PurchaseOrderLine,rec)._compute_analytic_id_and_tag_ids()
            rec.account_analytic_id = rec.order_id.picking_type_id.analytic_account_id


    def _prepare_stock_move_vals(self, picking, price_unit, product_uom_qty, product_uom):
        res = super(PurchaseOrderLine, self)._prepare_stock_move_vals(picking, price_unit, product_uom_qty, product_uom)
        if self.order_id.picking_type_id.analytic_account_id:
            res['analytic_account_id'] = self.order_id.picking_type_id.analytic_account_id.id
        return res

