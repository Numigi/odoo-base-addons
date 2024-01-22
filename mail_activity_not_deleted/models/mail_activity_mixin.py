# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MailActivityMixin(models.AbstractModel):

    _inherit = 'mail.activity.mixin'

    # auto_join prevents the active filter from being automatically applied.
    activity_ids = fields.One2many(auto_join=False)
