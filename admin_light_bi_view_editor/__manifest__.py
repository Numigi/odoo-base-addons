# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/AGPL).

{
    'name': 'Admin Light BI View Editor',
    'version': "14.0.1.0.0",
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'AGPL-3',
    'category': 'Other',
    'summary': 'Add restrictions on the menu of bi_view_editor module.',
    'depends': [
        'admin_light_base',
        'bi_view_editor'
    ],
    'data': [
        'views/bi_view_editor_menu.xml',
    ],
    'installable': True,
}
