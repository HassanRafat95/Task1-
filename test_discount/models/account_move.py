from odoo import fields, models ,api
class AccountMove(models.Model):
    _inherit = 'account.move'

    discount_account_id = fields.Many2one(related='company_id.allowed_discount_account_id')
    discount_product_id = fields.Many2one(related='company_id.allowed_discount_product_id')

    sub_total_discount_allowed = fields.Float(compute="_compute_discount_allowed")

    @api.depends('invoice_line_ids')
    def _compute_discount_allowed(self):
        self.sub_total_discount_allowed = 0
        print("--------------------------------------------------------")
        for record in self:
            print("--------------------------------------------------------")
            print(record.invoice_line_ids)
            for line in self.invoice_line_ids:
                print(line.product_id.id + " - " + self.discount_product_id.id)
                if line.product_id.id == self.discount_product_id.id:
                    print("--------------------------------------------------------")
                    self.sub_total_discount_allowed = self.partner_id.allowed_discount * line.quantity
        print("--------------------------------------------------------")
        print("last value",self.sub_total_discount_allowed)

    def _discount_move_line(self):

        for invoice in self:
            if invoice.is_invoice(include_receipts=True):
                if invoice.partner_id.allowed_discount > 0 and invoice.move_type == 'out_invoice':
                    total_discount = 0
                    check_product = False
                    for line in invoice.line_ids:
                        if line.name == invoice.discount_product_id.name:
                            check_product = True
                            amount = line.credit / (invoice.discount_product_id.list_price - invoice.partner_id.allowed_discount)
                            total_discount = amount * invoice.partner_id.allowed_discount
                            line.credit += total_discount
                    if check_product:
                        create_method = invoice.env['account.move.line'].new or invoice.env[
                                'account.move.line'].create
                        candidate = create_method({
                                'name': invoice.discount_product_id.name + ' discount ',
                                'debit': total_discount,
                                'credit':  0.0,
                                'quantity': 1.0,
                                'move_id': invoice.id,
                                'currency_id': invoice.currency_id.id,
                                'account_id': invoice.discount_account_id.id,
                                'partner_id': invoice.commercial_partner_id.id,
                                'exclude_from_invoice_tab': True,
                            })







    def _recompute_dynamic_lines(self, recompute_all_taxes=False, recompute_tax_base_amount=False):
        ''' Recompute all lines that depend of others.

        For example, tax lines depends of base lines (lines having tax_ids set). This is also the case of cash rounding
        lines that depend of base lines or tax lines depending the cash rounding strategy. When a payment term is set,
        this method will auto-balance the move with payment term lines.

        :param recompute_all_taxes: Force the computation of taxes. If set to False, the computation will be done
                                    or not depending of the field 'recompute_tax_line' in lines.
        '''
        for invoice in self:
            # Dispatch lines and pre-compute some aggregated values like taxes.
            for line in invoice.line_ids:
                if line.recompute_tax_line:
                    recompute_all_taxes = True
                    line.recompute_tax_line = False

            # Compute taxes.
            if recompute_all_taxes:
                invoice._recompute_tax_lines()
            if recompute_tax_base_amount:
                invoice._recompute_tax_lines(recompute_tax_base_amount=True)

            if invoice.is_invoice(include_receipts=True):

                # Compute discount
                self._discount_move_line()
                # Compute cash rounding.
                invoice._recompute_cash_rounding_lines()

                # Compute payment terms.
                invoice._recompute_payment_terms_lines()

                # Compute

                # Only synchronize one2many in onchange.
                if invoice != invoice._origin:
                    invoice.invoice_line_ids = invoice.line_ids.filtered(lambda line: not line.exclude_from_invoice_tab)



