# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime, timedelta
from ddt import data, ddt
from odoo import models
from odoo.addons.queue_job.job import job
from odoo.tests.common import SavepointCase
from uuid import uuid4
from ..models.queue_job import TIME_LIMIT_PARAMETER


class ResPartner(models.Model):

    _inherit = 'res.partner'

    @job
    def _my_custom_job_method(self):
        pass


@ddt
class TestQueueJob(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.job = cls.env['queue.job'].create({
            'uuid': str(uuid4()),
            'user_id': cls.env.user.id,
            'state': 'pending',
            'model_name': 'res.partner',
            'method_name': '_my_custom_job_method',
            'record_ids': [cls.env.user.partner_id.id],
            'args': tuple(),
        })

        # Set time limit to 10 minutes
        cls.env['ir.config_parameter'].set_param(TIME_LIMIT_PARAMETER, 600)

        cls.time_exceeded = datetime.now() - timedelta(seconds=600)
        cls.time_not_exceeded = datetime.now() - timedelta(seconds=500)

    def _run_cron(self):
        self.env.ref('queue_job_auto_requeue.auto_requeue_cron').method_direct_trigger()

    @data('failed', 'done')
    def test_if_job_done_or_failed__job_not_requeued(self, state):
        self.job.write({
            'state': state,
            'date_started': self.time_exceeded,
            'date_enqueued': self.time_exceeded,
        })
        self._run_cron()
        assert self.job.state == state

    def test_if_time_enqueue_not_exceeded__job_not_requeued(self):
        self.job.write({
            'state': 'enqueued',
            'date_started': self.time_exceeded,
            'date_enqueued': self.time_not_exceeded,
        })
        self._run_cron()
        assert self.job.state == 'enqueued'

    def test_if_time_started_not_exceeded__job_not_requeued(self):
        self.job.write({
            'state': 'started',
            'date_started': self.time_not_exceeded,
            'date_enqueued': self.time_exceeded,
        })
        self._run_cron()
        assert self.job.state == 'started'

    def test_if_time_enqueue_exceeded__job_requeued(self):
        self.job.write({
            'state': 'enqueued',
            'date_started': self.time_not_exceeded,
            'date_enqueued': self.time_exceeded,
        })
        self._run_cron()
        assert self.job.state == 'pending'

    def test_if_time_started_exceeded__job_requeued(self):
        self.job.write({
            'state': 'started',
            'date_started': self.time_exceeded,
            'date_enqueued': self.time_not_exceeded,
        })
        self._run_cron()
        assert self.job.state == 'pending'
