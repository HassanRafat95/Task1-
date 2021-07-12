from odoo import fields, models,api
from datetime import date, timedelta,datetime

class PurchaseRequest(models.Model):
    _name = "purchase.request"
    RequestName = fields.Char(string="Request Name", required=True)
    RequestedBy = fields.Many2one("res.users",required=True,default=lambda self: self.env.user)
    StartDate = fields.Date('Start Date', default=fields.Date.today())
    EndDate = fields.Date('End Date')
    RejectionReason = fields.Text(string="Rejection Reason",readony=True)
    orderlines = fields.One2many("purchase.request.line", "order_id")
    TotalPrice = fields.Float(string="Total Price",compute="_compute_total",store=True)
    status = fields.Selection([
        ('draft','Draft'),
        ('to be approved','To Be Approved'),
        ('approve','Approve'),
        ('reject','Reject'),
        ('cancel', 'Cancel'),
    ]
    ,string="status",default="draft")


    @api.depends("orderlines.Total")
    def _compute_total(self):
        sum = 0;
        for orderline in self.orderlines:
            sum += orderline.Total
            self.TotalPrice = sum;

    def Submit_for_Approval(self):
        for record in self:
            record.status = "to be approved"
        return True

    def Cancel(self):
        for record in self:
            record.status = "cancel"
        return True

    def Approve(self):
        for record in self:
            record.status = "approve"
            tempelate_id = self.env.ref('purchase_request.request_template_mail');
            if tempelate_id:
                group_user = self.env.ref('purchase.group_purchase_manager').users
                for user_d in group_user:
                    tempelate_id.send_mail(self.id, force_send=True, raise_exception=True,
                                       email_values={'email_to': user_d.email})
        return True

    def Reset_to_draft(self):
        for record in self:
            record.status = "draft"
        return True





