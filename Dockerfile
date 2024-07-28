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

COPY attachment_minio /mnt/extra-addons/attachment_minio
COPY base_external_report_layout /mnt/extra-addons/base_external_report_layout
COPY ir_attachment_access_token_portal /mnt/extra-addons/ir_attachment_access_token_portal
COPY lang_fr_activated /mnt/extra-addons/lang_fr_activated
COPY mail_template_default /mnt/extra-addons/mail_template_default

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
