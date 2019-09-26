FROM quay.io/numigi/odoo-public:12.latest
MAINTAINER numigi <contact@numigi.com>

USER root

ARG GIT_TOKEN

COPY .docker_files/test-requirements.txt ./test-requirements.txt
RUN pip3 install -r ./test-requirements.txt && rm ./test-requirements.txt

ENV THIRD_PARTY_ADDONS /mnt/third-party-addons
RUN mkdir -p "${THIRD_PARTY_ADDONS}" && chown -R odoo "${THIRD_PARTY_ADDONS}"
COPY ./gitoo.yml /gitoo.yml
RUN gitoo install-all --conf_file /gitoo.yml --destination "${THIRD_PARTY_ADDONS}"

USER odoo

COPY auditlog /mnt/extra-addons/auditlog
COPY base_extended_security /mnt/extra-addons/base_extended_security
COPY disable_install_from_website /mnt/extra-addons/disable_install_from_website
COPY ir_attachment_access_token_portal /mnt/extra-addons/ir_attachment_access_token_portal
COPY ir_attachment_name_autocomplete /mnt/extra-addons/ir_attachment_name_autocomplete
COPY mail_activity_not_deleted /mnt/extra-addons/mail_activity_not_deleted
COPY mail_follower_picker /mnt/extra-addons/mail_follower_picker
COPY menu_item_rename /mnt/extra-addons/menu_item_rename
COPY note_no_default_stage /mnt/extra-addons/note_no_default_stage
COPY queue_job_auto_requeue /mnt/extra-addons/queue_job_auto_requeue
COPY super_calendar /mnt/extra-addons/super_calendar
COPY web_email_field_new_tab /mnt/extra-addons/web_email_field_new_tab

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
