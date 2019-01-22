# © 2015 ABF OSIELL <https://osiell.com>
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': "Audit Log",
    'version': "1.0.0",
    'author': "Numigi,ABF OSIELL,Odoo Community Association (OCA)",
    'license': "AGPL-3",
    'website': "https://www.osiell.com",
    'category': "Tools",
    'depends': [
        'base',
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/auditlog_log.xml',
        'views/auditlog_log_line.xml',
        'views/auditlog_rule.xml',
        'views/http_request.xml',
        'views/menu.xml',
    ],
    'application': True,
    'installable': True,
}
