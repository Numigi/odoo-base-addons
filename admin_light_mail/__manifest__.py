# Copyright 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Admin Light Email",
    "version": "16.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "LGPL-3",
    "category": "Other",
    "summary": "Add email management to the Admin Light application.",
    "depends": [
        "admin_light_base",
        "mail",
    ],
    "data": [
        "views/common.xml",
        "views/email_and_messages.xml",
        "views/mail_message_subtype.xml",
        "views/mail_server.xml",
        "views/mail_template.xml",
        "security/ir_rule_data.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
