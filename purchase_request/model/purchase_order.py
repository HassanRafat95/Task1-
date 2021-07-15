from odoo import api, fields,_,models

class PurchaseOrder(models.Model):
    #_name = "purchase.order"
    _inherit = ['purchase.order']
    _description = "Purchase Order"
    purchase_request_id = fields.Many2one("purchase.request")

    def action_view_request(self):
        return {
                'type': 'ir.actions.act_window',
                'name': _('request'),
                'res_model': 'purchase.request',
                'view_mode': 'tree,form',
                'domain': [(self.id, 'in', 'purchase_order_ids')],
        }