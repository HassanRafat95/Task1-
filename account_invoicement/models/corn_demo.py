from odoo import models,fields

class DemoClass(models.Model):
   _name = 'cron.demo'
   def calc_total_invoiced(self):
      partners_ids = self.env['res.partner']._search([])
      for partner_id in partners_ids :
         partner = self.env['res.partner'].browse(partner_id)
         partner.invoices_total=0;
         for invoice in partner.invoice_ids:
            if invoice.move_type  !='entry':
               if invoice.move_type == 'in_invoice' or invoice.move_type == 'out_refund':# purchase invoice & customer credit note
                  partner.invoices_total = partner.invoices_total - invoice.amount_total
               if invoice.move_type == 'out_invoice' or invoice.move_type == 'in_refund':# customer invoice & purchase credit note
                  partner.invoices_total = partner.invoices_total + invoice.amount_total
