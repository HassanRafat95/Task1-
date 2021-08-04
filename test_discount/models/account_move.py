from odoo import fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    discount_account_id = fields.Many2one(related='company_id.allowed_discount_account_id')
    discount_product_id = fields.Many2one(related='company_id.allowed_discount_product_id')

    sub_total_discount_allowed=fields.Float(compute="_compute_total")

    def _compute_total(self):
        for record in self:
            for line in self.invoice_line_ids:
                if line.product_id == self.discount_product_id:
                    self.sub_total_discount_allowed = self.partner_id.allowed_discount * line.quantity


    def _move_autocomplete_invoice_lines_values(self):
        print("--------------------------------------------------------------")
        rec= super(AccountMove, self)._move_autocomplete_invoice_lines_values()
        print(rec)
        print("--------------------------------------------------------------")
        print(self.move_type)
        move_line_id = 0
        vals = []
        if self.partner_id.allowed_discount > 0 and self.move_type == 'out_invoice':
            for line in self.line_ids:
                if line.account_id.id == 42:
                    line.credit += self.partner_id.allowed_discount
                #vals.append([0, 0, {
                 #       'id': line.id,
                 #       'account_id': line.account_id,
                #      'credit': line.credit,
                 #       'debit': line.debit,
                  #      }])

        # vals.append([0, 0, {
         #               'account_id': self.discount_account_id,
          #              'credit': 0,
           #             'debit': self.partner_id.allowed_discount,
            #            }])
        #print(vals)
        #print("_______________________")
        #self.line_ids.create({
        #                'account_id': self.discount_account_id.id,
        #               'credit': 0,
        #               'debit': self.partner_id.allowed_discount,
        #               'move_id': self.id})
        #print("_______________________")
        #print(self.line_ids)
        #rec['line_ids'] = self.line_ids
        return rec
