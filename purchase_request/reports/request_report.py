from odoo import api, models




class PurchaseRequestReport(models.AbstractModel):
    _name = 'report.purchase_request.report_purchase_inherit_demo'
    _description = 'purchase request as PDF.'

    def _get_report_values(self, docids, data=None):
        print("hi")
        docs = self.env['purchase.request'].browse(docids[0])
        test = " Value come from def Get_Report_Values"
        return {
            'doc_model':'purchase.request',
            'data' : data,
            'docs' : docs,
            'test' : test,
        }


