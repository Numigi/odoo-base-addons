FROM quay.io/numigi/odoo-public:12.latest
MAINTAINER numigi <contact@numigi.com>

USER odoo

COPY auditlog /mnt/extra-addons/auditlog
COPY ir_attachment_access_token_portal /mnt/extra-addons/ir_attachment_access_token_portal
COPY ir_attachment_name_autocomplete /mnt/extra-addons/ir_attachment_name_autocomplete
COPY mail_activity_not_deleted /mnt/extra-addons/mail_activity_not_deleted
COPY mail_follower_picker /mnt/extra-addons/mail_follower_picker
COPY note_no_default_stage /mnt/extra-addons/note_no_default_stage
COPY super_calendar /mnt/extra-addons/super_calendar

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
