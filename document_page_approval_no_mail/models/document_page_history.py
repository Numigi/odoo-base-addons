# © 2021 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models

CONTEXT_VAR = "document_page_history_no_email"


class DocumentPageHistory(models.Model):

    _inherit = "document.page.history"

    def action_to_approve(self):
        self = self._with_force_internal_note()
        return super(DocumentPageHistory, self).action_to_approve()

    def action_approve(self):
        self = self._with_force_internal_note()
        return super(DocumentPageHistory, self).action_approve()

    def action_cancel(self):
        self = self._with_force_internal_note()
        return super(DocumentPageHistory, self).action_cancel()

    def message_post(
        self, body="", subject=None, message_type="notification", subtype=None, **kwargs
    ):
        if self._should_force_internal_note():
            subtype = "mail.mt_note"
            message_type = "notification"

        return super().message_post(
            body=body,
            subject=subject,
            message_type=message_type,
            subtype=subtype,
            **kwargs
        )

    def message_post_with_template(self, template_id, **kwargs):
        if self._should_force_internal_note():
            kwargs = dict(
                kwargs,
                subtype_id=self.env.ref("mail.mt_note").id,
                message_type="notification",
            )
        return super().message_post_with_template(template_id, **kwargs)

    def _with_force_internal_note(self):
        return self.with_context(**{CONTEXT_VAR: True})

    def _should_force_internal_note(self):
        return self._context.get(CONTEXT_VAR)
