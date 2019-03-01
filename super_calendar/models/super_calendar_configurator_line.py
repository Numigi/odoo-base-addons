# © 2012 Agile Business Group sagl (<http://www.agilebg.com>)
# © 2012 Domsense srl (<http://www.domsense.com>)
# © 2015 Anubía, soluciones en la nube,SL (http://www.anubia.es)
#                Alejandro Santana <alejandrosantana@anubia.es>
# © 2015 Savoir-faire Linux <http://www.savoirfairelinux.com>)
#                Agathe Mollé <agathe.molle@savoirfairelinux.com>
# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, date
from pytz import timezone
from mako.template import Template
from odoo import _, api, exceptions, fields, models
from odoo.models import BaseModel
from odoo.osv.expression import AND
from odoo.tools.safe_eval import safe_eval
from typing import Optional


def _get_datetime_field_value_in_user_tz(record: BaseModel, field_name: str) -> Optional[datetime]:
    """Get a datetime field value in the timezone of the user.

    In case of a date field, the timezone from the context is used to convert
    the date into a datetime with 00:00:00.
    """
    value = record[field_name]
    tz = timezone(record._context.get('tz') or record.env.user.tz or 'UTC')

    is_date_value = isinstance(value, date) and not isinstance(value, datetime)

    if is_date_value:
        datetime_value = datetime(value.year, value.month, value.day)
        local_datetime_value = tz.localize(datetime_value)
    else:
        local_datetime_value = tz.localize(value)

    return local_datetime_value


class SuperCalendarConfiguratorLine(models.Model):

    _name = 'super.calendar.configurator.line'
    _description = 'Super Calendar Configurator Line'

    name = fields.Many2one(
        comodel_name='ir.model',
        string='Model',
        required=True,
    )
    domain = fields.Char(
        string='Domain',
    )
    configurator_id = fields.Many2one(
        comodel_name='super.calendar.configurator',
        string='Configurator',
    )
    description_type = fields.Selection(
        [('field', 'Field'),
         ('code', 'Code')],
        string="Description Type",
        default='field',
    )
    description_field_id = fields.Many2one(
        comodel_name='ir.model.fields',
        string='Description Field',
        domain="[('ttype', 'in', ('char', 'text')), ('model_id', '=', name)]",
    )
    description_code = fields.Text(
        string='Description Code',
        help=("""Use '${o}' to refer to the involved object.
E.g.: '${o.project_id.name}'"""),
    )
    date_start_field_id = fields.Many2one(
        comodel_name='ir.model.fields',
        string='Start Date Field',
        domain="[('ttype', 'in', ('datetime', 'date')), "
               "('model_id', '=', name)]",
        required=True,
    )
    date_stop_field_id = fields.Many2one(
        comodel_name='ir.model.fields',
        string='End Date Field',
        domain="[('ttype', 'in', ('datetime', 'date')), "
               "('model_id', '=', name)]",
    )
    duration_field_id = fields.Many2one(
        comodel_name='ir.model.fields',
        string='Duration Field',
        domain="[('ttype', '=', 'float'), ('model_id', '=', name)]",
    )
    user_field_id = fields.Many2one(
        comodel_name='ir.model.fields',
        string='User Field',
        domain="[('ttype', '=', 'many2one'), ('model_id', '=', name)]",
    )
    last_cron_update = fields.Datetime()

    def _get_domain(self):
        """Get the domain to apply to the super calendar."""
        return self.domain and safe_eval(self.domain) or []

    def _delete_all_calendar_events(self):
        """Delete all calendar events related to the configurator self."""
        self.env['super.calendar'].search([('configurator_line_id', 'in', self.ids)]).unlink()

    def _delete_events_related_to_updated_records(self):
        """Delete all events related to records updated since last cron."""
        domain = AND([self._get_domain(), [('write_date', '>=', self.last_cron_update)]])
        records = self.env[self.name.model].search(domain)
        record_references = ['{},{}'.format(self.name.model, r.id) for r in records]
        deprecated_events = self.env['super.calendar'].search([
            ('configurator_line_id', 'in', self.ids),
            ('res_id', 'in', record_references),
        ])
        deprecated_events.unlink()

    @api.multi
    def write(self, vals):
        """Remove old events on write.

        The next time the cron is ran, all records will be recomputed.
        """
        vals['last_cron_update'] = False
        return super().write(vals)

    def _get_calendar_event_name(self, record):
        """Get the name to display on the calendar event.

        :param record: the record related to the calendar event.
        :rtype: Optional[str]
        """
        if self.description_type == 'code':
            parse_dict = {'o': record}
            mytemplate = Template(self.description_code)
            return mytemplate.render(**parse_dict)
        else:
            return record[self.description_field_id.name]

    def _get_calendar_event_user_id(self, record):
        """Get the user id for the calendar event.

        :param record: the record related to the calendar event.
        :rtype: Optional[int]
        """
        user_field_name = self.user_field_id.name
        if not user_field_name:
            return None

        user = record[user_field_name]

        if user and user._name != 'res.users':
            raise exceptions.ValidationError(
                _("The 'User' field of record %s (%s) does not refer to res.users")
                % (user_field_name, self.name.model))

        return user.id if user else None

    def _get_calendar_event_record_reference(self, record):
        """Get the reference of the record related to the calendar event.

        Recurrent events have an string id like '14-20151110120000'
        We split this value to get the first part (id).

        :param record: the record related to the calendar event.
        :rtype: str
        """
        if isinstance(record['id'], str):
            record_id = record['id'].split('-')[0]
        else:
            record_id = record['id']
        return '{},{}'.format(self.name.model, record_id)

    @api.multi
    def _get_calendar_event_duration(self, record):
        """Get the duration of a calendar event record.

        :param record: the record related to the calendar event.
        :rtype: Optional[int]
        """
        uses_duration = bool(self.duration_field_id)
        uses_date_stop = bool(self.date_stop_field_id)

        if uses_duration:
            return record[self.duration_field_id.name]
        elif uses_date_stop:
            datetime_start = _get_datetime_field_value_in_user_tz(
                record, self.date_start_field_id.name)
            datetime_stop = _get_datetime_field_value_in_user_tz(
                record, self.date_stop_field_id.name)
            return (datetime_stop - datetime_start).total_seconds() / 3600
        else:
            return None

    @api.multi
    def _get_calendar_event_values(self, record):
        """Get the values for a super calendar event.

        :param record: the record related to the calendar event.
        :rtype: dict
        """
        return {
            'name': self._get_calendar_event_name(record),
            'date_start': _get_datetime_field_value_in_user_tz(
                record, self.date_start_field_id.name),
            'duration': self._get_calendar_event_duration(record),
            'user_id': self._get_calendar_event_user_id(record),
            'configurator_id': self.configurator_id.id,
            'configurator_line_id': self.id,
            'res_id': self._get_calendar_event_record_reference(record),
            'model_id': self.name.id,
        }

    @api.multi
    def generate_calendar_records(self):
        """Generate / update calendar records."""
        if self.last_cron_update:
            self._delete_events_related_to_updated_records()
        else:
            self._delete_all_calendar_events()

        domain = AND([self._get_domain(), [(self.date_start_field_id.name, '!=', False)]])

        if self.last_cron_update:
            domain = AND([domain, [('write_date', '>=', self.last_cron_update)]])

        records_to_process = self.env[self.name.model].search(domain)

        for record in records_to_process:
            self.env['super.calendar'].create(self._get_calendar_event_values(record))

        self.last_cron_update = datetime.now()

        return True
