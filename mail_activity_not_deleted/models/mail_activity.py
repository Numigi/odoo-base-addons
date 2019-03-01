# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

from odoo import api, fields, models


class MailActivityInactivatedInsteadOfDeleted(models.Model):

    _inherit = 'mail.activity'

    active = fields.Boolean(default=True)
    date_done = fields.Datetime()

    def action_feedback(self, feedback=False):
        self = self.with_context(mail_activity_no_delete=True)
        return super(MailActivityInactivatedInsteadOfDeleted, self).action_feedback(False)

    @api.multi
    def unlink(self):
        """Deactivate instead of deleting the activity when it is completed."""
        if self._context.get('mail_activity_no_delete'):
            self._send_signal_done()
            self.write({
                'active': False,
                'date_done': datetime.now(),
            })
            for activity in self:
                activity._update_record_date_deadline()
        else:
            return super().unlink()

    def _send_signal_done(self):
        """Send the signal to the chatter that the activity has been completed.

        The code in this method was extracted odoo/addons/mail/models/mail_activity.py.
        """
        for activity in self:
            if activity.date_deadline <= fields.Date.today():
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', activity.user_id.partner_id.id),
                    {'type': 'activity_updated', 'activity_deleted': True})

    def _update_record_date_deadline(self):
        """Update the stored fields that depend on activity_ids on the related record."""
        record = self.env[self.res_model].browse(self.res_id)
        record.modified(['activity_ids'])
        record.recompute()


class MailActivityWithStateDone(models.Model):
    """Add the state done to mail activities."""

    _inherit = 'mail.activity'

    state = fields.Selection(selection_add=[('done', 'Done')])

    @api.depends('date_deadline')
    def _compute_state(self):
        super()._compute_state()

        done_activities = self.filtered(lambda a: a.date_done)
        for activity in done_activities:
            activity.state = 'done'


class MailActivityMixinWithActivityNotDeletedWhenRecordDeactivated(models.AbstractModel):
    """When deactivating a record, deactivate activities instead of deleting them."""

    _inherit = 'mail.activity.mixin'

    # auto_join prevents the active filter from being automatically applied.
    activity_ids = fields.One2many(auto_join=False)

    @api.multi
    def write(self, vals):
        if 'active' in vals and vals['active'] is False:
            self = self.with_context(mail_activity_no_delete=True)
        return super(MailActivityMixinWithActivityNotDeletedWhenRecordDeactivated, self).write(vals)
