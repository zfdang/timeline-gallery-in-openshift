/*
 * jQuery File Upload Plugin JS Example 7.0
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/*jslint nomen: true, unparam: true, regexp: true */
/*global $, window, document */

$(function () {
    'use strict';

    // https://github.com/blueimp/jQuery-File-Upload/wiki/API
    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload({
        // Uncomment the following to send cross-domain cookies:
        // xhrFields: {withCredentials: true},
        // use form.action
        // url: '/admin/uploads/'
    });

    // Demo settings:
    $('#fileupload').fileupload('option', {
        maxFileSize: 5000000,
        // acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
        process: [
            {
                action: 'load',
                fileTypes: /^image\/(gif|jpeg|png)$/,
                maxFileSize: 20000000 // 20MB
            },
            {
                action: 'resize',
                maxWidth: 1440,
                maxHeight: 900
            },
            {
                action: 'save'
            }
        ]
    });

    // Load existing files:
    // $.ajax({
    //     // Uncomment the following to send cross-domain cookies:
    //     // xhrFields: {withCredentials: true},
    //     url: $('#fileupload').fileupload('option', 'url'),
    //     dataType: 'json',
    //     context: $('#fileupload')[0]
    // }).done(function (result) {
    //     $(this).fileupload('option', 'done')
    //         .call(this, null, {result: result});
    // });

});
