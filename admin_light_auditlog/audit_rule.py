# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class AuditRule(models.Model):
    """Use sudo when subscribing/unsubscribing an audit rule.

    The mechanism of creating/deleting the action in the form view
    uses multiple objects that the admin/light should not be able
    to access.
    """

    _inherit = 'auditlog.rule'

    def unsubscribe(self):
        if self.env.user.has_group('admin_light_auditlog.group_auditlogs'):
            self = self.sudo()

        return super(AuditRule, self).unsubscribe()

    def subscribe(self):
        if self.env.user.has_group('admin_light_auditlog.group_auditlogs'):
            self = self.sudo()

        return super(AuditRule, self).subscribe()
