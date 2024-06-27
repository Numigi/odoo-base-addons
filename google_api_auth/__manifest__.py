# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Google API Authentication",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://bit.ly/numigi-com",
    "license": "AGPL-3",
    "category": "Hidden/Tools",
    "external_dependencies": {
        "python": [
            "google-api-python-client",
            "google-auth-httplib2",
            "google-auth-oauthlib",
        ]
    },
    "depends": ["base"],
    "summary": "Allow users to connect to Google applications.",
    "data": [
        "security/ir.model.access.csv",
        "views/google_application_views.xml",
    ],
    "installable": True,
}
