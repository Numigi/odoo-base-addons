# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Auth Oauth Microsoft",
    "version": "1.2.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "LGPL-3",
    "category": "Other",
    "summary": "Allow to login with Microsoft",
    "external_dependencies": {"python": ["PyJWT"]},
    "depends": ["auth_oauth"],
    "data": [
        "data/auth_oauth_provider.xml",
        "views/auth_oauth_views.xml",
        "views/auth_oauth_templates.xml",
    ],
    "installable": True,
}
