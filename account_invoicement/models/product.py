from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = "product.product"
    default_code = fields.Char('Internal Reference', index=True,compute="_compute_default_code",store=True)

    @api.depends("categ_id.code", "categ_id.complete_name", "product_tmpl_id.mfi_code","product_tmpl_id.density_code")
    def _compute_default_code(self):
        self.default_code = self.categ_id._get_categ_parents_code(self.categ_id)+self.product_tmpl_id.mfi_code+self.product_tmpl_id.density_code

