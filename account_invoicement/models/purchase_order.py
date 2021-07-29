from odoo import fields, models, api
from odoo.exceptions import AccessError


class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']

    total_discount = fields.Float(compute="_compute_total")
    primary_total = fields.Float(compute="_compute_total")

    @api.depends("order_line.product_qty", "order_line.price_unit", "order_line.discount")
    def _compute_total(self):
        for record in self:
            record.primary_total = sum((l.product_qty * l.price_unit) for l in record.order_line)
            record.total_discount = sum((l.product_qty * l.price_unit * (l.discount / 100)) for l in record.order_line)

    def _add_supplier_to_product(self):
        # Add the partner in the supplier list of the product if the supplier is not registered for
        # this product. We limit to 10 the number of suppliers for a product to avoid the mess that
        # could be caused for some generic products ("Miscellaneous").
        for line in self.order_line:
            # Do not add a contact as a supplier
            partner = self.partner_id if not self.partner_id.parent_id else self.partner_id.parent_id
            if line.product_id and partner not in line.product_id.seller_ids.mapped('name') and len(
                    line.product_id.seller_ids) <= 10:
                # Convert the price in the right currency.
                currency = partner.property_purchase_currency_id or self.env.company.currency_id
                price_after_discount = line.price_unit * ((100 - line.discount) / 100)
                price = self.currency_id._convert(price_after_discount, currency, line.company_id,
                                                  line.date_order or fields.Date.today(), round=False)
                # Compute the price for the template's UoM, because the supplier's UoM is related to that UoM.
                if line.product_id.product_tmpl_id.uom_po_id != line.product_uom:
                    default_uom = line.product_id.product_tmpl_id.uom_po_id
                    price = line.product_uom._compute_price(price, default_uom)

                supplierinfo = {
                    'name': partner.id,
                    'sequence': max(
                        line.product_id.seller_ids.mapped('sequence')) + 1 if line.product_id.seller_ids else 1,
                    'min_qty': 0.0,
                    'price': price,
                    'currency_id': currency.id,
                    'delay': 0,
                }
                # In case the order partner is a contact address, a new supplierinfo is created on
                # the parent company. In this case, we keep the product name and code.
                seller = line.product_id._select_seller(
                    partner_id=line.partner_id,
                    quantity=line.product_qty,
                    date=line.order_id.date_order and line.order_id.date_order.date(),
                    uom_id=line.product_uom)
                if seller:
                    supplierinfo['product_name'] = seller.product_name
                    supplierinfo['product_code'] = seller.product_code
                vals = {
                    'seller_ids': [(0, 0, supplierinfo)],
                }
                try:
                    line.product_id.write(vals)
                except AccessError:  # no write access rights -> just ignore
                    break


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

    @api.depends('product_qty', 'price_unit', 'taxes_id', 'discount')
    def _compute_amount(self):
        for line in self:
            vals = line._prepare_compute_all_values()
            vals['price_unit'] = vals['price_unit'] * ((100 - line.discount) / 100)
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
        res = super(PurchaseOrderLine, self)._prepare_account_move_line()
        res['discount'] = self.discount
        if self.order_id.picking_type_id.analytic_account_id:
            res['analytic_account_id'] = self.order_id.picking_type_id.analytic_account_id.id
        return res

    @api.depends('product_id', 'date_order')
    def _compute_analytic_id_and_tag_ids(self):
        for rec in self:
            super(PurchaseOrderLine, rec)._compute_analytic_id_and_tag_ids()
            rec.account_analytic_id = rec.order_id.picking_type_id.analytic_account_id

    def _prepare_stock_move_vals(self, picking, price_unit, product_uom_qty, product_uom):
        res = super(PurchaseOrderLine, self)._prepare_stock_move_vals(picking, price_unit, product_uom_qty, product_uom)
        if self.order_id.picking_type_id.analytic_account_id:
            res['analytic_account_id'] = self.order_id.picking_type_id.analytic_account_id.id
        return res
