# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Meeting Minutes",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "AGPL-3",
    "category": "Other",
    "depends": ["base"],
    "summary": "Add an abstract model, which can be used on several objects in Odoo.",
    "data": [
        'security/ir.model.access.csv',
        "views/meeting_minutes_mixin_views.xml",
        "views/means_communication_views.xml",
    ],
    "installable": True,
}
