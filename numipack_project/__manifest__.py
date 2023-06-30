# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Numipack - Project',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Functional dependencies for all Odoo instances using sales.',
    'depends': [
        'numipack',

        # odoo/odoo
        'hr_timesheet',
        'project',

        # Numigi / odoo-project-addons
        'project_default_task_stage',  # TA#34544
        'project_list',  # TA#55010
        'project_stage_no_quick_create',
        'project_task_date_planned',
        'project_task_full_text_search',
        'project_task_stage_external_mail',  # TA#15910
        'project_task_type',
        'project_type',
    ],
    'data': [
        'data/auditlog_rule.xml',
        'security/extended_security_rule.xml',
    ],
    'installable': True,
}
