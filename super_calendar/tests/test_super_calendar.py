# © 2012 Agile Business Group sagl (<http://www.agilebg.com>)
# © 2012 Domsense srl (<http://www.domsense.com>)
# © 2015 Anubía, soluciones en la nube,SL (http://www.anubia.es)
#                Alejandro Santana <alejandrosantana@anubia.es>
# © 2015 Savoir-faire Linux <http://www.savoirfairelinux.com>)
#                Agathe Mollé <agathe.molle@savoirfairelinux.com>
# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from pytz import timezone
from odoo.tests import SavepointCase
from datetime import datetime
from dateutil.relativedelta import relativedelta


class TestSuperCalendar(SavepointCase):

    def setUp(self):
        super().setUp()
        self.partner_a = self.env['res.partner'].create({
            'name': 'Partner A',
            'date': (datetime.today() + relativedelta(days=3)),
        })
        self.partner_b = self.env['res.partner'].create({'name': 'Partner B'})

        self.configurator = self.env['super.calendar.configurator'].create({'name': 'Partners'})

        self.partner_model = self.env['ir.model'].search([
            ('model', '=', 'res.partner')
        ])
        self.date_start_field = self.env['ir.model.fields'].search([
            ('name', '=', 'write_date'),
            ('model', '=', 'res.partner'),
        ])
        self.description_field = self.env['ir.model.fields'].search([
            ('name', '=', 'name'),
            ('model', '=', 'res.partner'),
        ])

        self.configurator_line = self.env['super.calendar.configurator.line'].create({
            'name': self.partner_model.id,
            'date_start_field_id': self.date_start_field.id,
            'description_field_id': self.description_field.id,
            'configurator_id': self.configurator.id,
        })

    def _generate_calendar_event(self, partner):
        values = self.configurator.line_ids._get_calendar_event_values(partner)
        return self.env['super.calendar'].create(values)

    def test_generate_event_with_no_duration(self):
        event = self._generate_calendar_event(self.partner_a)
        assert event.date_start == self.partner_a.write_date
        assert event.name == self.partner_a.name
        assert event.model_id == self.partner_model
        assert event.res_id == self.partner_a
        assert not event.duration
        assert not event.user_id

    def test_generate_event_with_stop_date(self):
        date_stop_field = self.env['ir.model.fields'].search([
            ('name', '=', 'date'),
            ('model', '=', 'res.partner'),
        ])
        self.configurator_line.date_stop_field_id = date_stop_field.id
        event = self._generate_calendar_event(self.partner_a)

        tz = timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')

        start_datetime = tz.localize(self.partner_a.write_date)

        stop_date = self.partner_a.date
        stop_datetime = tz.localize(datetime(stop_date.year, stop_date.month, stop_date.day))

        date_diff = (stop_datetime - start_datetime)
        expected_duration = date_diff.total_seconds() / 3600

        assert round(event.duration, 6) == round(expected_duration, 6)

    def test_generate_event_with_description_code(self):
        self.configurator_line.write({
            'description_type': 'code',
            'description_code': '${o.email}',
        })
        partner_email = 'super-calendar@test.com'
        self.partner_a.email = partner_email
        event = self._generate_calendar_event(self.partner_a)
        assert event.name == partner_email

    def _find_event(self, partner):
        return self.env['super.calendar'].search([
            ('res_id', '=', 'res.partner,{}'.format(partner.id)),
        ])

    def test_super_calendar_generator_cron(self):
        self.env['super.calendar.configurator'].generate_calendar_records()
        event = self._find_event(self.partner_a)
        assert event.name == self.partner_a.name

    def test_configuration_line_domain(self):
        self.configurator_line.domain = [('name', '=', self.partner_a.name)]
        self.env['super.calendar.configurator'].generate_calendar_records()
        event_a = self._find_event(self.partner_a)
        event_b = self._find_event(self.partner_b)
        assert event_a
        assert not event_b

    def test_on_unlink_then_event_is_unlinked(self):
        self.env['super.calendar.configurator'].generate_calendar_records()
        event_a = self._find_event(self.partner_a)
        event_b = self._find_event(self.partner_b)
        self.partner_a.unlink()
        assert not event_a.exists()
        assert event_b.exists()

    def _write_partner_values(self, partner, vals):
        """Simulate a write to a partner record from a distinct transaction.

        Update the write_date manually, otherwise, it is set to the begining of
        the current transaction.
        """
        partner.write(vals)
        self.env.cr.execute(
            'UPDATE res_partner SET write_date = %s WHERE id = %s',
            (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), partner.id))

    def test_on_record_write_then_event_is_updated(self):
        self.env['super.calendar.configurator'].generate_calendar_records()
        event = self._find_event(self.partner_a)
        assert event.name == self.partner_a.name

        new_name = 'New Name'
        self._write_partner_values(self.partner_a, {'name': new_name})

        self.env['super.calendar.configurator'].generate_calendar_records()
        event = self._find_event(self.partner_a)

        assert event.name == new_name

    def test_on_configurator_write_then_all_events_unlinked(self):
        self.configurator_line.name = self.env.ref('base.model_res_partner')
        events = self.env['super.calendar'].search([
            ('configurator_line_id', '=', self.configurator_line.id),
        ])
        assert not events

        # On the next cron, the calendar is completely regenerated.
        self.env['super.calendar.configurator'].generate_calendar_records()
        events = self.env['super.calendar'].search([
            ('configurator_line_id', '=', self.configurator_line.id),
        ])
        assert events
