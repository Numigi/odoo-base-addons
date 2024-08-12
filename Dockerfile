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
COPY auth_oauth_microsoft /mnt/extra-addons/auth_oauth_microsoft
COPY auth_session_redis_timeout /mnt/extra-addons/auth_session_redis_timeout
COPY base_extended_security /mnt/extra-addons/base_extended_security
COPY base_extended_security_grid /mnt/extra-addons/base_extended_security_grid
COPY base_meeting_minutes /mnt/extra-addons/base_meeting_minutes
COPY base_selection_label /mnt/extra-addons/base_selection_label
COPY base_view_mode_restricted /mnt/extra-addons/base_view_mode_restricted
COPY base_xml_rename /mnt/extra-addons/base_xml_rename
COPY currency_rate_update_boc /mnt/extra-addons/currency_rate_update_boc
COPY disable_install_from_website /mnt/extra-addons/disable_install_from_website
COPY dms_document_url /mnt/extra-addons/dms_document_url
COPY document_page_approval_no_mail /mnt/extra-addons/document_page_approval_no_mail
COPY helpdesk_mgmt_no_mail /mnt/extra-addons/helpdesk_mgmt_no_mail
COPY helpdesk_ticket_phone /mnt/extra-addons/helpdesk_ticket_phone
COPY ir_attachment_access_token_portal /mnt/extra-addons/ir_attachment_access_token_portal
COPY ir_attachment_name_autocomplete /mnt/extra-addons/ir_attachment_name_autocomplete
COPY ir_attachment_ressource_editable /mnt/extra-addons/ir_attachment_ressource_editable
COPY mail_activity_list_mark_done /mnt/extra-addons/mail_activity_list_mark_done
COPY mail_activity_not_deleted /mnt/extra-addons/mail_activity_not_deleted
COPY mail_bot_no_pong /mnt/extra-addons/mail_bot_no_pong
COPY mail_follower_picker /mnt/extra-addons/mail_follower_picker
COPY mail_message_from_author /mnt/extra-addons/mail_message_from_author
COPY mail_notification_no_action_button /mnt/extra-addons/mail_notification_no_action_button
COPY mail_notification_no_footer /mnt/extra-addons/mail_notification_no_footer
COPY mail_recipient_unchecked /mnt/extra-addons/mail_recipient_unchecked
COPY mail_template_archive /mnt/extra-addons/mail_template_archive
COPY mail_template_default /mnt/extra-addons/mail_template_default
COPY note_no_default_stage /mnt/extra-addons/note_no_default_stage
COPY portal_attachment /mnt/extra-addons/portal_attachment
COPY portal_signature_auto /mnt/extra-addons/portal_signature_auto
COPY private_data_group /mnt/extra-addons/private_data_group
COPY queue_job_auto_requeue /mnt/extra-addons/queue_job_auto_requeue
COPY super_calendar /mnt/extra-addons/super_calendar
COPY test_http_request /mnt/extra-addons/test_http_request
COPY url_link_type /mnt/extra-addons/url_link_type
COPY users_access_token /mnt/extra-addons/users_access_token
COPY utm_archive /mnt/extra-addons/utm_archive
COPY web_email_field_new_tab /mnt/extra-addons/web_email_field_new_tab

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
