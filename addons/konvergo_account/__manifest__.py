# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Konvergo / Accounting',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Accounting Dependencies for Konvergo',
    'depends': [
        # Numigi/odoo-base
        'konvergo_base',
        'numipack_account',

        # Numigi/odoo-account-addons
        'account_show_full_features',  # TA#16549

        # OCA/mis-builder
        'mis_builder',  # TA#16549

        # OCA/reporting-engine
        'report_xlsx',  # TA#16549 (dependency of mis_builder)

        # OCA/server-ux
        'date_range',  # TA#16549 (dependency of mis_builder)

        # OCA/web
        'web_widget_color',  # TA#16549 (dependency of mis_builder)

        # OCA/account-financial-reporting
        'account_export_csv',  # TA#16549
        'account_financial_report',  # TA#16549
        'account_tax_balance',  # TA#16549
        'mis_builder_cash_flow',  # TA#16549
        'partner_statement',  # TA#16549

        # akretion
        'account_viewer',  # TA#16549
        'account_report_viewer',  # TA#16549
    ],
    'installable': True,
}
