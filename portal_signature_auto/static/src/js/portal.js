odoo.define("portal_signature_auto.signature_form", function(require) {
"use strict";

const ajax = require("web.ajax");
const core = require("web.core");
const qweb = core.qweb;
const SignatureForm = require("portal.signature_form").SignatureForm;

SignatureForm.include({

    events: Object.assign({}, SignatureForm.prototype.events, {
        "click #o_portal_draw_auto": "drawCurrentName",
    }),

    _loadTemplates() {
        return $.when(this._super(), ajax.loadXML("/portal_signature_auto/static/src/xml/portal.xml", qweb));
    },

    drawCurrentName: function (event) {
        event.preventDefault()
        event.stopPropagation()
        this._clearCanvas()
        this._drawNameOnCanvas()
        const signature = this._getCanvasDataURL()
        this.$("#o_portal_signature").jSignature("reset");
        this.$("#o_portal_signature").jSignature("importData", signature);
    },

    initSign() {
        this._super.apply(this, arguments);
        const context = this._getCanvasContext()
        context.font = "60px Italianno";
        context.fillText("", 0, 0);
    },

    _clearCanvas() {
        const ctx = this._getCanvasContext()
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    },

    _drawNameOnCanvas() {
        const ctx = this._getCanvasContext()
        const name = this.$("#o_portal_sign_name").val()
        const width = ctx.measureText(name).width;
        ctx.fillText(name, 60, 100);
    },

    _getCanvasDataURL() {
        const canvas = this._getCanvas()
        return canvas.toDataURL()
    },

    _getCanvasContext() {
        return this._getCanvas().getContext("2d");
    },

    _getCanvas() {
        return this.$("#signature_canvas")[0]
    },
});

});
