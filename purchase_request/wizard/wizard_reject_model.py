from odoo import models,fields,api
from datetime import date, timedelta,datetime
class wizard_reject (models.TransientModel):
    _name = "wizard.reject"
    _description = "wizard  reject confirm "
    rejection_reason = fields.Char(string="Rejection Reason",required=True)

    def confirm(self):
        print(self.env['purchase.request'].browse(self.env.context.get('active_id')))
        self.env['purchase.request'].browse(self.env.context.get('active_id')).write({
            'RejectionReason':self.rejection_reason,
            'status':'reject'
        });
        return True


