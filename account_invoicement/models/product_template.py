from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = "product.template"
    mfi_code = fields.Text(string='MFI Code')
    density_code = fields.Text(string='Density Code')
