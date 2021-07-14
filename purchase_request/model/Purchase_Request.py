from odoo import fields, models,api, _
from datetime import date, timedelta,datetime
from odoo.exceptions import UserError

class PurchaseRequest(models.Model):
    _name = "purchase.request"

    name = fields.Char(string="Request Name", required=True)
    requested_by = fields.Many2one("res.users",required=True,default=lambda self: self.env.user)
    start_date = fields.Date('Start Date', default=fields.Date.today())
    end_date = fields.Date('End Date')
    rejection_reason = fields.Text(string="Rejection Reason",readony=True)
    order_line_ids = fields.One2many("purchase.request.line", "order_id")
    total_price = fields.Float(string="Total Price",compute="_compute_total",store=True)
    status = fields.Selection([
        ('draft','Draft'),
        ('to be approved','To Be Approved'),
        ('approve','Approve'),
        ('reject','Reject'),
        ('cancel', 'Cancel'),
    ]
    ,string="status",default="draft")
    purchase_orders_count = fields.Integer(compute="_compute_order_count")


    @api.depends("order_line_ids.total")
    def _compute_total(self):
        for record in self:
            record.total_price = sum(l.total for l in record.order_line_ids)
            # sum = 0
            # for order_line in self.order_line_ids:
            #     sum += order_line.Total
            #     self.total_price = sum

    def _compute_order_count(self):
        for rec in self:
            rec.purchase_orders_count = self.env['purchase.order'].search_count([('purchase_request_id','=',rec.id),('state','not in',['draft','cancel'])])

    def action_submit_for_approval(self):
        for record in self:
            record.status = "to be approved"
        return True

    def action_cancel(self):
        for record in self:
            record.status = "cancel"
        return True

    def action_approve(self):
        for record in self:
            record.status = "approve"
            #tempelate_id = self.env.ref('purchase_request.request_template_mail');
            #if tempelate_id:
                #group_user = self.env.ref('purchase.group_purchase_manager').users
                #for user_d in group_user:
                   # tempelate_id.send_mail(self.id, force_send=True, raise_exception=True,
                   #                    email_values={'email_to': user_d.email})
        return True

    def action_reset_to_draft(self):
        for record in self:
            record.status = "draft"
        return True

    def action_print_report(self):
        return self.env.ref("purchase_request.purchase_request_report").report_action(self)

    def action_create_order(self):
        for record in self:
            if record.purchase_orders_count >= 2:
                raise UserError(_("you can not have more than two purchase orders per purchase request"))
            else:
                vals = []
                purchase_order = self.env['purchase.order']
                for order_line in record.order_line_ids:
                    vals.append([0, 0, {
                        'name': order_line.description,
                        'product_qty': order_line.quantity,
                        'product_id': order_line.product_id.id,
                        'price_unit': order_line.cost_price}])
                purchase_order.create({
                    'name': record.name,
                    'partner_id': record.requested_by.id,
                    'invoice_status': 'no',
                    'purchase_request_id': record.id,
                    'order_line': vals
                })
        return True

    def action_view_orders(self):
        return {
                'type': 'ir.actions.act_window',
                'name': _('orders'),
                'res_model': 'purchase.order',
                'view_mode': 'tree,form',
                'domain': [('purchase_request_id', '=', self.id)],
        }
