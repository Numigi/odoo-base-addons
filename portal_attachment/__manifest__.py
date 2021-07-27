# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Portal Attachment",
    "category": "Website",
    "summary": "Allow to upload attachments from the customer portal.",
    "license": "LGPL-3",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "depends": ["portal"],
    "data": [
        "views/templates.xml",
    ],
    "qweb": ["static/src/xml/*.xml"],
    "installable": True,
}
