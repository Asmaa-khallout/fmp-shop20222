/* Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
odoo.define('website_voucher.website_voucher', function (require) {
	'use strict';

	var publicWidget = require('web.public.widget');
	publicWidget.registry.websiteCoupon = publicWidget.Widget.extend({
		selector: '.o_portal_my_doc_table',
		events: {
			'click .copy_code': '_onClickCopyCode',
		},
		_onClickCopyCode: function (ev) {
			var $fa = $(ev.currentTarget);
			var $temp = $("<input>");
			$("body").append($temp);
			$temp.val($fa.parent().siblings(".code_input").text().trim()).select();
			document.execCommand("copy");
			$temp.remove();
			$('.copy_code').html('<i class="fa fa-solid fa-copy"/>');
			$('.copy_code').attr('class','copy_code btn btn-danger rounded-pill');
			$fa.html('<i class="fa fa-solid fa-check"/>');
			$fa.attr('class','copy_code btn btn-success rounded-pill');
		},
	});
});
