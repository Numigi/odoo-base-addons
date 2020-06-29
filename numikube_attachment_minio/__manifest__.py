# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "NumiKube Attachment Minio",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "LGPL-3",
    "category": "Other",
    "summary": "Attachment Minio for the Numigi Kubernetes infrastructure",
    "depends": ["attachment_minio", "numikube_minio"],
    "data": ["data/ir_config_parameter.xml",],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
