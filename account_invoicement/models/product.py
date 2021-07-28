from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = "product.product"
    default_code = fields.Char('Internal Reference', index=True,compute="_compute_default_code",store=True)

    @api.depends("categ_id.code", "categ_id.complete_name", "product_tmpl_id.mfi_code","product_tmpl_id.density_code")
    def _compute_default_code(self):
        self.default_code = self._get_categ_parents_code()+self.product_tmpl_id.mfi_code+self.product_tmpl_id.density_code

    def _get_categ_parents_code(self,categ):
        code =''
        for category in self:
            if category.parent_id:
                code = self._get_categ_parents_code(self,categ) + categ.code
            else:
                return code


