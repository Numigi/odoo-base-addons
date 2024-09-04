# Copyright 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Admin Light Audit Logs",
    "version": "16.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "LGPL-3",
    "category": "Other",
    "summary": "Add a group to manage audit logs.",
    "depends": ["admin_light_base", "auditlog"],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/menus.xml",
    ],
    "installable": True,
}
