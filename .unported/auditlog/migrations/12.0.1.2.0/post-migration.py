# © 2021 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


def migrate(env, version):
    if not version:
        return

    env.execute("""
        ALTER TABLE auditlog_rule DROP CONSTRAINT auditlog_rule_model_uniq
    """)
