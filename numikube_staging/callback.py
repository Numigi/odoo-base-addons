# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


def run_callback(env, job_id, data):
    job = _get_job(env, job_id)
    job.sudo().run_callback(data)


def _get_job(env, job_id):
    return env["staging.job"].browse(job_id)
