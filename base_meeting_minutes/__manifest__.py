# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Base Meeting Minutes",
    "version": "12.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "AGPL-3",
    "category": "Other",
    "depends": ["contacts"],
    "summary": "Meeting Minutes base model",
    "data": [
        "security/ir.model.access.csv",
        "templates/meeting_minutes_mixin_templates.xml",
        "views/meeting_channel_views.xml",
        "views/meeting_minutes_mixin_views.xml",
        "views/menus.xml",
        "views/reports.xml",
        "views/res_partner_views.xml",
    ],
    "installable": True,
}
