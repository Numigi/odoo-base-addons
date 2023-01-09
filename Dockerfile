FROM quay.io/numigi/odoo-public:14.latest
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
COPY auth_oauth_authentik /mnt/extra-addons/auth_oauth_authentik
COPY automatic_activity_deadlines /mnt/extra-addons/automatic_activity_deadlines
COPY base_extended_security /mnt/extra-addons/base_extended_security
COPY base_extended_security_grid /mnt/extra-addons/base_extended_security_grid
COPY base_selection_label /mnt/extra-addons/base_selection_label
COPY base_view_mode_restricted /mnt/extra-addons/base_view_mode_restricted
COPY base_xml_rename /mnt/extra-addons/base_xml_rename
#COPY helpdesk_ticket_phone /mnt/extra-addons/helpdesk_ticket_phone
COPY ir_attachment_access_token_portal /mnt/extra-addons/ir_attachment_access_token_portal
COPY ir_attachment_name_autocomplete /mnt/extra-addons/ir_attachment_name_autocomplete
#COPY lang_fr_activated /mnt/extra-addons/lang_fr_activated
COPY mail_activity_list_mark_done /mnt/extra-addons/mail_activity_list_mark_done
COPY mail_activity_not_deleted /mnt/extra-addons/mail_activity_not_deleted
COPY mail_bot_no_pong /mnt/extra-addons/mail_bot_no_pong
#COPY mail_follower_picker /mnt/extra-addons/mail_follower_picker
#COPY mail_notification_no_action_button /mnt/extra-addons/mail_notification_no_action_button
COPY mail_message_from_author /mnt/extra-addons/mail_message_from_author
COPY mail_notification_no_footer /mnt/extra-addons/mail_notification_no_footer
#COPY mail_template_archive /mnt/extra-addons/mail_template_archive
COPY mail_template_default /mnt/extra-addons/mail_template_default
COPY note_no_default_stage /mnt/extra-addons/note_no_default_stage
#COPY private_data_group /mnt/extra-addons/private_data_group
#COPY queue_job_auto_requeue /mnt/extra-addons/queue_job_auto_requeue
COPY test_http_request /mnt/extra-addons/test_http_request
#COPY url_link_type /mnt/extra-addons/url_link_type
COPY utm_archive /mnt/extra-addons/utm_archive
COPY web_email_field_new_tab /mnt/extra-addons/web_email_field_new_tab

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
