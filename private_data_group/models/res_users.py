# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class User(models.Model):

    _inherit = 'res.users'

    def has_private_data_access(self):
        return self.has_group('private_data_group.group_private_data')
