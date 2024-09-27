# Copyright 2022-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def _set_default_group_members(env):
    """Set default members of group Manage Private Information.

    When installing the module, members of HR / Manager are set as members
    of the group Manage Private Information.

    However, there is no requirement that HR / Manager have access to private data.
    """
    manager_group_members = env.ref('hr.group_hr_manager').users
    private_information_group = env.ref('private_data_group.group_private_data')

    _logger.info(
        'Setting users {} as members of the group Manage Private Information.'
        .format(manager_group_members.mapped('login'))
    )
    manager_group_members.write({
        'groups_id': [(4, private_information_group.id)],
    })


def _deactivate_private_address_ir_rule(env):
    _logger.info('Deactivating legacy access rules related to private addresses.')
    env.ref('base.res_partner_rule_private_employee').active = False
    env.ref('base.res_partner_rule_private_group').active = False


def post_init(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _set_default_group_members(env)
    _deactivate_private_address_ir_rule(env)
