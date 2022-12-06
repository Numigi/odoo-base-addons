# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
from odoo.addons.web.controllers.main import ExportFormat, CSVExport, ExcelExport
from odoo.http import request
from odoo.osv.expression import AND


class ExportFormatWithSecurityDomain(ExportFormat):

    def base(self, data, token):
        params = json.loads(data)
        record_ids = params.get('ids')
        model = params['model']

        if record_ids:
            records = request.env[model].browse(record_ids)
            records.check_extended_security_read()
        else:
            search_domain = params.get('domain') or []
            security_domain = request.env[model].get_extended_security_domain()
            params['domain'] = AND((search_domain, security_domain))
            data = json.dumps(params)

        return super().base(data, token)


class CSVControllerWithSecurity(CSVExport, ExportFormatWithSecurityDomain):
    pass


class ExcelExportWithSecurity(ExcelExport, ExportFormatWithSecurityDomain):
    pass
