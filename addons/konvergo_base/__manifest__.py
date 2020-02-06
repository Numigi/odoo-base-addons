# © 2020 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Konvergo',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Dependencies for Konvergo',
    'depends': [
        # Numigi/odoo-base
        'numipack',
        'numitech',
        # commented for now. It is not compatible with konvergo_login_page
        # see TA#17781
        # 'odoo-debrand',  # TA#16526
        'konvergo_favicon_title',  # TA#16527
        'konvergo_login_page',  # TA#18145
        'konvergo_cron_publisher',  # TA#16530

        # OCA/social
        'mail_debrand',  # TA#16549


        # theme
        'muk_web_theme',
    ],
    'installable': True,
}
