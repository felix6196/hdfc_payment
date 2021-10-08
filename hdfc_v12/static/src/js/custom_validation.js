odoo.define('HDFC.web_responsive', function(require) {
    'use strict';
    var ajax = require('web.ajax');
    $(document).ready(function() {
		var location_address = window.location.href;
        if (location_address.indexOf('/HDFC_payment/pay') > -1) {
            $('#HDFC_templates_form').submit();
            $('.auto-save').savy('load');
        }


    });

});
