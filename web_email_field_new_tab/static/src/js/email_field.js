// © Numigi (tm) and all its contributors (https://numigi.com/r/home)
// License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
odoo.define("web_field_widget_new_tab.email_field", function (require) {
"use strict";

var basicFields = require("web.basic_fields");

basicFields.FieldEmail.include({
    _renderReadonly() {
        this._super();
        this.$el.attr("target", "_blank");
    },
});

});
