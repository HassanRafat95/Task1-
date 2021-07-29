from odoo import models,api,fields
import random

class CornClass(models.Model):
    _name = 'cron'

    # defaults
    @api.model
    def _default_number(self):
        return 55.8

    number = fields.Float(string="Number", default=_default_number)

    def calc_total_invoiced(self):
        for partner in self.env['res.partner'].search([]):
            total_invoice = 0
            for invoice in partner.invoice_ids:
                if invoice.move_type != 'entry':
                    if invoice.move_type in ['in_invoice', 'out_refund']:  # purchase invoice & customer credit note
                        total_invoice -= invoice.amount_total
                    elif invoice.move_type in ['out_invoice', 'in_refund']:  # customer invoice & purchase credit note
                        total_invoice += invoice.amount_total
            partner.invoices_total = total_invoice

    @api.model
    def print_invoices_total(self):
        for partner in self.env['res.partner'].search([]):
            print("Partner Name = %s  - Total Invoice  %s" % (partner.name,partner.invoices_total))

    @api.model
    def print_thank_you(self,name):
        print("thank you  %s " % (name))



