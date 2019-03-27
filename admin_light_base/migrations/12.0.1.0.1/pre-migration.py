# © 2019 Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openupgradelib import openupgrade


def migrate(cr, installed_version):
    """Update the xml_id of Admin Light / Sequences.

    The group was moved to admin_light_base.
    This prevents blocking unique constraints when updating
    the modules.
    """
    openupgrade.rename_xmlids(
        cr,
        [('admin_light_specific.group_sequence',
          'admin_light_base.group_sequence')]
    )
