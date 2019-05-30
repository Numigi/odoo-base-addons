# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Numipack - Sales',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Functional dependencies for all Odoo instances using sales.',
    'depends': [
        # odoo/odoo
        'hr_timesheet',
        'project',

        # Numigi / odoo-project-addons
        'project_stage_no_quick_create',
        'project_task_date_planned',
        'project_task_full_text_search',
        'project_task_type',
        'project_type',
    ],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
