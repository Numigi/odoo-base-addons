# Copyright 2026-today Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields
import ast


class TranslationManagerWizard(models.TransientModel):
    _name = "data.translation.wizard"
    _description = "Mass Translation Manager"

    source_lang_id = fields.Many2one(
        comodel_name="res.lang",
        string="Source Language",
        required=True,
        help="Select the language from which the translations will be read.",
    )
    dest_lang_id = fields.Many2one(
        comodel_name="res.lang",
        string="Destination Language",
        required=True,
        help="Select the language to which the translations will be written.",
    )
    model_id = fields.Many2one(
        comodel_name="ir.model",
        string="Target Model",
        required=True,
        help="Select the Odoo model you want to process the translations for.",
    )
    model_name = fields.Char(
        related="model_id.model",
        string="Model Name",
        help="Technical name of the selected model.",
    )
    operation = fields.Selection(
        selection=[
            ("copy", "Copy"),
            ("export", "Export"),
            ("import", "Import"),
        ],
        string="Operation",
        required=True,
        default="copy",
        help="Choose the action to perform: Copy translations between languages, Export them, or Import them.",
    )
    fields_option = fields.Selection(
        selection=[
            ("all", "All Fields"),
            ("selection", "Select Fields"),
        ],
        string="Fields Processing",
        default="all",
        help="Choose if you want to process all translatable fields of the model or only a specific selection.",
    )
    field_ids = fields.Many2many(
        comodel_name="ir.model.fields",
        string="Translatable Fields",
        domain="[('model_id', '=', model_id), ('translate', '=', True)]",
        help="Select the specific translatable fields to process.",
    )
    data_option = fields.Selection(
        selection=[
            ("all", "All Records"),
            ("selection", "Selection"),
        ],
        string="Data Processing",
        default="all",
        help="Choose if you want to apply the operation on all records of the model or filter them using a domain.",
    )
    record_domain = fields.Char(
        string="Domain Filter",
        default="[]",
        help="Define the domain to filter the records that will be processed.",
    )

    def action_execute_operation(self):
        self._route_operation()

    def _route_operation(self):
        if self.operation == "copy":
            self._execute_copy_operation()
        if self.operation == "export":
            self._execute_export_operation()
        if self.operation == "import":
            self._execute_import_operation()

    def _execute_copy_operation(self):
        records = self._get_target_records()
        fields_to_process = self._get_target_fields()
        self._process_records_copy(records, fields_to_process)

    def _execute_export_operation(self):
        pass

    def _execute_import_operation(self):
        pass

    def _get_target_records(self):
        if self.data_option == "all":
            return self.env[self.model_name].search([])
        return self._get_records_from_domain()

    def _get_records_from_domain(self):
        domain = ast.literal_eval(self.record_domain or "[]")
        return self.env[self.model_name].search(domain)

    def _get_target_fields(self):
        if self.fields_option == "selection":
            return self.field_ids.mapped("name")
        return self._get_all_translatable_fields()

    def _get_all_translatable_fields(self):
        domain = [
            ("model_id", "=", self.model_id.id),
            ("translate", "=", True),
        ]
        return self.env["ir.model.fields"].search(domain).mapped("name")

    def _process_records_copy(self, records, fields_list):
        for record in records:
            self._update_single_record(record, fields_list)

    def _update_single_record(self, record, fields_list):
        source_record = record.with_context(lang=self.source_lang_id.code)
        update_vals = self._extract_update_values(source_record, record, fields_list)
        self._write_translations(record, update_vals)

    def _extract_update_values(self, source_record, target_record, fields_list):
        update_vals = {}
        for field in fields_list:
            self._evaluate_field_for_update(field, source_record, target_record, update_vals)
        return update_vals

    def _evaluate_field_for_update(self, field, source_record, target_record, update_vals):
        source_val = source_record[field]
        target_val = target_record.with_context(lang=self.dest_lang_id.code)[field]
        if source_val and source_val != target_val:
            update_vals[field] = source_val

    def _write_translations(self, record, update_vals):
        if update_vals:
            record.with_context(lang=self.dest_lang_id.code).write(update_vals)
