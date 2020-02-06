odoo.define("konvergo_favicon_title.title", function(require) {
    var WebClient = require("web.WebClient");


    WebClient.include({
        init: function(parent) {
            this._super.apply(this, arguments);
            this.set("title_part", {"zopenerp": "Konvergo"});
        }
    });

});