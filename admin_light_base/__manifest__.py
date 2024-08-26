# Copyright 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Admin Light",
    "version": "16.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "LGPL-3",
    "category": "Other",
    "summary": "Add an admin menu with restricted functionalities.",
    "depends": ["base"],
    "data": [
        "data/base.xml",
        "data/sequence.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
    "application": True,
}
