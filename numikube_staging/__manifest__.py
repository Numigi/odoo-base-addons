# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Numikube Staging",
    "version": "14.0.1.0.0",
    "author": "Numigi",
    "website": "https://github.com/Numigi/odoo-base",
    "maintainer": "Numigi",
    "license": "LGPL-3",
    "category": "Other",
    "summary": "Run staging from a remote odoo production environment",
    "depends": [
        "mail",
        "admin_light_base",
        "numikube_database_backup"
                ],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "data/mail_template.xml",
        "views/staging_environment.xml",
        "views/staging_job.xml",
        "views/menu.xml",
    ],
    "installable": True,
}
