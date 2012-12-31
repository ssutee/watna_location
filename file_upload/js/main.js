/*
 * jQuery File Upload Plugin JS Example 6.7
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

    $('#fileupload').fileupload();

    $('#fileupload').fileupload('option', {
      maxFileSize: 5000000,
      acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
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
    $('#fileupload').each(function () {
      console.log('load existing files');
      var that = this;
      $.getJSON(this.action, function (result) {
          if (result && result.length) {
              $(that).fileupload('option', 'done')
                  .call(that, null, {result: result});
          }
      });
    });
    

});
