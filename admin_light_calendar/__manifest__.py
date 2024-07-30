# Copyright 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Admin Light Calendar",
    "version": "16.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "LGPL-3",
    "category": "Other",
    "summary": "Add calendar objects to the Admin Light application.",
    "depends": ["admin_light_base", "calendar", "resource"],
    "data": [
        "data/res_groups.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
