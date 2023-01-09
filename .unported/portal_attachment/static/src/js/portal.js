odoo.define("portal_chatter_attachment.chatter", function(require) {
"use strict";

const ajax = require("web.ajax");
const core = require("web.core");
const qweb = core.qweb;
const PortalChatter = require("portal.chatter").PortalChatter;

PortalChatter.include({
    _loadTemplates() {
        return $.when(this._super(), ajax.loadXML("/portal_attachment/static/src/xml/portal.xml", qweb));
    },
});

});
