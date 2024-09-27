# Copyright 2022-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
from odoo.addons.web.controllers.export import ExportFormat, CSVExport, ExcelExport
from .common import check_model_fields_access, extract_fields_from_domain


class ExportFormatWithPrivateFields(ExportFormat):

    def base(self, data, token):
        params = json.loads(data)
        fields_to_check = {f['name'].replace('/', '.') for f in params['fields']}

        domain = params.get('domain')
        if domain:
            fields_to_check.update(extract_fields_from_domain(domain))

        model = params['model']
        check_model_fields_access(model, fields_to_check)
        return super().base(data, token)


class CSVControllerWithPrivateFields(CSVExport, ExportFormatWithPrivateFields):
    pass


class ExcelExportWithPrivateFields(ExcelExport, ExportFormatWithPrivateFields):
    pass
