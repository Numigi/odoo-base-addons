# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Portal Signature Auto",
    "category": "Website",
    "summary": "Allow to automatically fill a signature from the portal",
    "license": "LGPL-3",
    "version": "14.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "depends": ["portal"],
    "data": [
        "views/templates.xml",
    ],
    "qweb": ["static/src/xml/*.xml"],
    "installable": True,
}
