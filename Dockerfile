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

COPY admin_light_auditlog /mnt/extra-addons/admin_light_auditlog
COPY admin_light_base /mnt/extra-addons/admin_light_base
COPY admin_light_bi_view_editor /mnt/extra-addons/admin_light_bi_view_editor
COPY admin_light_calendar /mnt/extra-addons/admin_light_calendar
COPY admin_light_company /mnt/extra-addons/admin_light_company
COPY admin_light_filters /mnt/extra-addons/admin_light_filters
COPY admin_light_gamification /mnt/extra-addons/admin_light_gamification
COPY admin_light_mail /mnt/extra-addons/admin_light_mail
COPY admin_light_mail_gmail /mnt/extra-addons/admin_light_mail_gmail
COPY admin_light_mail_outlook /mnt/extra-addons/admin_light_mail_outlook
COPY admin_light_user /mnt/extra-addons/admin_light_user
COPY admin_light_web /mnt/extra-addons/admin_light_web
COPY auth_oauth_authentik /mnt/extra-addons/auth_oauth_authentik
COPY automatic_activity_deadlines /mnt/extra-addons/automatic_activity_deadlines
COPY base_extended_security /mnt/extra-addons/base_extended_security
COPY base_extended_security_grid /mnt/extra-addons/base_extended_security_grid
COPY base_external_report_layout /mnt/extra-addons/base_external_report_layout
COPY base_selection_label /mnt/extra-addons/base_selection_label
COPY base_view_mode_restricted /mnt/extra-addons/base_view_mode_restricted
COPY base_xml_rename /mnt/extra-addons/base_xml_rename
COPY currency_rate_update_boc /mnt/extra-addons/currency_rate_update_boc
COPY ir_attachment_access_token_portal /mnt/extra-addons/ir_attachment_access_token_portal
COPY lang_fr_activated /mnt/extra-addons/lang_fr_activated
COPY mail_activity_list_mark_done /mnt/extra-addons/mail_activity_list_mark_done
COPY mail_bot_no_pong /mnt/extra-addons/mail_bot_no_pong
COPY mail_notification_no_action_button /mnt/extra-addons/mail_notification_no_action_button
COPY mail_message_from_author /mnt/extra-addons/mail_message_from_author
COPY mail_notification_no_footer /mnt/extra-addons/mail_notification_no_footer
COPY mail_template_default /mnt/extra-addons/mail_template_default
COPY note_no_default_stage /mnt/extra-addons/note_no_default_stage
COPY numipack /mnt/extra-addons/numipack
COPY numipack_account /mnt/extra-addons/numipack_account
COPY numipack_account_enterprise /mnt/extra-addons/numipack_account_enterprise
COPY numipack_project /mnt/extra-addons/numipack_project
COPY numipack_purchase /mnt/extra-addons/numipack_purchase
COPY numipack_sale /mnt/extra-addons/numipack_sale
COPY numipack_stock /mnt/extra-addons/numipack_stock
COPY portal_signature_auto /mnt/extra-addons/portal_signature_auto
COPY profile_hr /mnt/extra-addons/profile_hr
COPY private_data_group /mnt/extra-addons/private_data_group
COPY queue_job_auto_requeue /mnt/extra-addons/queue_job_auto_requeue
COPY test_http_request /mnt/extra-addons/test_http_request
COPY utm_archive /mnt/extra-addons/utm_archive
COPY web_email_field_new_tab /mnt/extra-addons/web_email_field_new_tab
COPY dms_document_url /mnt/extra-addons/dms_document_url
COPY event_allowed_ceu /mnt/extra-addons/event_allowed_ceu
COPY web_base_url_freeze /mnt/extra-addons/web_base_url_freeze

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
