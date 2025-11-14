# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Numigi crm test",
    "version": "1.0.0",
    "author": "Youness LOUARMASSI",
    "maintainer": "Numigi",
    "license": "LGPL-3",
    "category": "Other",
    "summary": "Custom development on CRM module",
    "depends": ["crm", "website_crm"],
    "data": [
        "security/crm_security.xml",
        "data/crm_data.xml",
        "data/mail_data.xml",
        "data/service_cron.xml",
        "views/crm_team_views.xml",
        "views/crm_lead_views.xml"
        ],
    "installable": True,
    'post_init_hook': 'crm_refresh_res_setting',
}
