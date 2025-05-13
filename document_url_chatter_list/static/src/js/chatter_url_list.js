/* Copyright 2023 Numigi
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
 */
odoo.define("document_url_chatter_list.UrlAttachmentList", function (require) {
    "use strict";

    var core = require('web.core');
    var QWeb = core.qweb;
    var FormController = require('web.FormController');
    var _t = core._t;

    /**
     * Add URL attachments section to the chatter
     * Using FormController to ensure we have access to the model and record
     */
    FormController.include({
        /**
         * @override
         */
        _onAttachmentChange: function() {
            this._super.apply(this, arguments);
            this._updateUrlAttachments();
        },

        /**
         * @override
         */
        _update: function() {
            var self = this;
            return this._super.apply(this, arguments).then(function() {
                self._updateUrlAttachments();
                return $.when();
            });
        },

        /**
         * @override
         */
        renderButtons: function() {
            this._super.apply(this, arguments);
            // Ensure we update on initial render
            var self = this;
            // Wait a bit for the form to be fully rendered
            setTimeout(function() {
                self._updateUrlAttachments();
            }, 1000);
        },

        /**
         * Find URL attachments and display them
         */
        _updateUrlAttachments: function() {
            var self = this;
            
            // Check if we're in a form view
            if (!this.renderer || !this.renderer.$el || !this.model || !this.model.localData) {
                console.log("Not in a form view context");
                return;
            }
            
            // Get the current record ID
            var handle = this.handle;
            if (!handle || !this.model.localData[handle]) {
                console.log("No active record");
                return;
            }
            
            var record = this.model.localData[handle];
            var modelName = record.model;
            var recordID = record.res_id;
            
            if (!recordID) {
                console.log("No record ID (might be a new record)");
                return;
            }
            
            // Find the chatter
            var $chatter = this.renderer.$el.find('.o_form_sheet_bg + .oe_chatter, .oe_chatter');
            if (!$chatter.length) {
                console.log("No chatter found on this form");
                return;
            }
            
            // Use RPC to fetch attachments with creation date
            this._rpc({
                model: 'ir.attachment',
                method: 'search_read',
                domain: [
                    ['res_model', '=', modelName],
                    ['res_id', '=', recordID],
                ],
                fields: ['id', 'name', 'url', 'mimetype', 'type', 'create_date'],
                context: {active_test: false},
            }).then(function(allAttachments) {
                
                // Filter URL attachments manually
                var urlAttachments = _.filter(allAttachments, function(attachment) {
                    return attachment.mimetype === 'application/link' || 
                           attachment.type === 'url' ||
                           (attachment.url && attachment.url !== '');
                });
                
                if (urlAttachments && urlAttachments.length > 0) {
                    try {
                        // Format dates for display
                        _.each(urlAttachments, function(attachment) {
                            if (attachment.create_date) {
                                var date = new Date(attachment.create_date);
                                attachment.formatted_date = date.toLocaleDateString();
                            } else {
                                attachment.formatted_date = '';
                            }
                        });
                        
                        // Render the URL attachments section as a table
                        var $urlSection = $(QWeb.render('document_url_chatter_list.UrlAttachmentList', {
                            attachments: urlAttachments,
                        }));
                        
                        // Find mail thread for insertion point
                        var $mailThread = $chatter.find('.o_mail_thread');
                        
                        var insertionPoint;
                        if ($mailThread.length) {
                            insertionPoint = $mailThread;
                        } else {
                            // Fallback to activities or chatter itself
                            var $activity = $chatter.find('.o_mail_activity');
                            if ($activity.length) {
                                insertionPoint = $activity;
                            } else {
                                insertionPoint = $chatter;
                                // Using append instead of before
                                $chatter.find('.o_chatter_url_attachments').remove();
                                var $urlContainer = $('<div class="o_chatter_url_attachments mb-3"></div>');
                                $chatter.append($urlContainer);
                                $urlContainer.append($urlSection);
                                
                                // Add click handler for URLs
                                $urlContainer.find('.o_attachment_url_link').click(function(e) {
                                    var url = $(this).attr('href');
                                    if (url) {
                                        window.open(url, '_blank');
                                    }
                                    e.preventDefault();
                                    e.stopPropagation();
                                });
                                return; // Skip the normal insertion code below
                            }
                        }
                        
                        // Remove any existing container
                        $chatter.find('.o_chatter_url_attachments').remove();
                        
                        // Create container and insert section
                        var $urlContainer = $('<div class="o_chatter_url_attachments mb-3"></div>');
                        insertionPoint.before($urlContainer);
                        $urlContainer.append($urlSection);
                        
                        // Add click handler for URLs
                        $urlContainer.find('.o_attachment_url_link').click(function(e) {
                            var url = $(this).attr('href');
                            if (url) {
                                window.open(url, '_blank');
                            }
                            e.preventDefault();
                            e.stopPropagation();
                        });
                    } catch (err) {
                        console.error("Error rendering URL attachments:", err);
                    }
                } else {
                    // Remove any existing URL container
                    $chatter.find('.o_chatter_url_attachments').remove();
                }
            }).fail(function(error) {
                console.error("Error fetching URL attachments:", error);
            });
        },
    });

    // Debug message to confirm script is loaded
    console.log("Chatter URL List extension loaded with FormController integration");
});