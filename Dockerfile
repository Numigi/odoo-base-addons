FROM quay.io/numigi/odoo-public:16.latest
LABEL maintainer="contact@numigi.com"

USER root

COPY .docker_files/test-requirements.txt ./test-requirements.txt
RUN pip3 install -r ./test-requirements.txt && rm ./test-requirements.txt

ENV THIRD_PARTY_ADDONS /mnt/third-party-addons
RUN mkdir -p "${THIRD_PARTY_ADDONS}" && chown -R odoo "${THIRD_PARTY_ADDONS}"
COPY ./gitoo.yml /gitoo.yml
RUN gitoo install-all --conf_file /gitoo.yml --destination "${THIRD_PARTY_ADDONS}"

USER odoo

COPY base_extended_security /mnt/extra-addons/base_extended_security
COPY admin_light_auditlog /mnt/extra-addons/admin_light_auditlog
COPY admin_light_base /mnt/extra-addons/admin_light_base
COPY admin_light_bi_view_editor /mnt/extra-addons/admin_light_bi_view_editor
COPY admin_light_calendar /mnt/extra-addons/admin_light_calendar
COPY admin_light_company /mnt/extra-addons/admin_light_company
COPY admin_light_gamification /mnt/extra-addons/admin_light_gamification
COPY admin_light_mail /mnt/extra-addons/admin_light_mail
COPY admin_light_mail_gmail /mnt/extra-addons/admin_light_mail_gmail
COPY admin_light_mail_outlook /mnt/extra-addons/admin_light_mail_outlook
COPY admin_light_web /mnt/extra-addons/admin_light_web
COPY admin_light_filters /mnt/extra-addons/admin_light_filters
COPY attachment_minio /mnt/extra-addons/attachment_minio
COPY lang_fr_activated /mnt/extra-addons/lang_fr_activated
COPY mail_notification_no_action_button /mnt/extra-addons/mail_notification_no_action_button
COPY mail_template_default /mnt/extra-addons/mail_template_default
COPY private_data_group /mnt/extra-addons/private_data_group
COPY test_http_request /mnt/extra-addons/test_http_request

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
