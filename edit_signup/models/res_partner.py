from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    date_of_birth = fields.Date(string='Date of Birth')
    is_mature = fields.Boolean(string='Is Mature', compute="_check_is_mature", readonly=True)

    def _check_is_mature(self):
        for rec in self:
            if rec.date_of_birth:
                dt = str(rec.date_of_birth)
                d1 = datetime.strptime(dt, "%Y-%m-%d").date()
                d2 = date.today()
                rd = relativedelta(d2, d1)

                if rd.years >= 18:
                    rec.is_mature = True
                else:
                    rec.is_mature = False
            else:
                rec.is_mature = False
