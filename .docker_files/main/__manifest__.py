# © 2024 Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Main Module",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Other",
    "summary": "Install all addons required for testing.",
    "depends": [
        "base",
        "account",  # required for testing auditlog
        "sale",  # required for testing mail_message_from_author
        "stock",  # required for testing base_extended_security
        "crm",  # required for testing mail_notification_no_action_button
    ],
    "installable": True,
}
