# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'HR Profile',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Dependencies for the HR profile',
    'depends': [
        # odoo/odoo
        'hr_contract',
        'hr_holidays',
        'hr_org_chart',

        # Numigi/odoo-hr-addons
        'hr_contract_wage_type',
        'hr_event',

        # OCA/hr
        'hr_employee_firstname',
        'hr_employee_phone_extension',

        # OCA/partner-contact
        'partner_firstname',  # dependency of hr_employee_firstname
    ],
    'installable': True,
}
