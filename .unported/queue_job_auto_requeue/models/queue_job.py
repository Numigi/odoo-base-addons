# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from datetime import datetime, timedelta
from odoo import api, models

_logger = logging.getLogger(__name__)


DEFAULT_JOB_TIME_LIMIT = 300
TIME_LIMIT_PARAMETER = 'queue_job_time_limit'


class QueueJob(models.Model):

    _inherit = 'queue.job'

    @api.model
    def auto_requeue_cron(self):
        started_jobs = self.env['queue.job'].search([('state', '=', 'started')])
        enqueued_jobs = self.env['queue.job'].search([('state', '=', 'enqueued')])

        time_limit = self.env['ir.config_parameter'].get_param(
            TIME_LIMIT_PARAMETER, DEFAULT_JOB_TIME_LIMIT)

        min_time = datetime.now() - timedelta(seconds=int(time_limit))

        stalled_jobs = (
            started_jobs.filtered(lambda j: j.date_started < min_time) |
            enqueued_jobs.filtered(lambda j: j.date_enqueued < min_time)
        )

        for job in stalled_jobs:
            _logger.info(
                'Resetting job {} to pending because it seems to be stalled.'
                .format(job.uuid)
            )
            job.requeue()
