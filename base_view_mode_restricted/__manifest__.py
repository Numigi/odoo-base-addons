# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Base View Mode Restricted",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "LGPL-3",
    "category": "Other",
    "summary": "Add view mode restrictions on window actions",
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/ir_actions_act_window.xml",
    ],
    "installable": True,
}
