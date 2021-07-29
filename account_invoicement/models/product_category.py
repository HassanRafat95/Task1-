from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"
    code = fields.Text(string='Code')

    def _get_categ_parents_code(self, categ):
        code = ''
        for category in categ:
            if category.parent_id:
                if category.code:
                    code = self._get_categ_parents_code(category.parent_id) + category.code
                else:
                    code = self._get_categ_parents_code(category.parent_id)
                return code
            else:
                if category.code:
                    code = category.code
                return code
        return code
