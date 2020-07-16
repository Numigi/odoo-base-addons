# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "NumiKube Database Backup",
    "version": "1.1.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "LGPL-3",
    "category": "Other",
    "summary": "Database Backups for the Numigi Kubernetes infrastructure",
    "depends": ["base", "numikube_minio"],
    "data": ["data/ir_cron.xml",],
    "installable": True,
}
