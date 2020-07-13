//$(document).bind('toolbar_setup', function() {
//	$('.navbar-home').html('<img class="erpnext-icon" src="'+
//			frappe.urllib.get_base_url()+'/assets/styling/images/logo.jpg" />');
//});
$(document).bind('toolbar_setup', function() {
	frappe.app.name = "Solubis";

	frappe.help_feedback_link = '<p><a class="text-muted" \
		href="solubis.id">Visit Us</a></p>'


	//$('[data-link="docs"]').attr("href", "https://erpnext.com/docs")
	//$('[data-link="issues"]').attr("href", "https://github.com/frappe/erpnext/issues")


	// default documentation goes to erpnext
	// $('[data-link-type="documentation"]').attr('data-path', '/erpnext/manual/index');

	// additional help links for erpnext
	//var $help_menu = $('.dropdown-help ul .documentation-links');
	//$('<li><a data-link-type="forum" href="https://erpnext.com/docs/user/manual" \
	//	target="_blank">'+__('Documentation')+'</a></li>').insertBefore($help_menu);
	//$('<li><a data-link-type="forum" href="https://discuss.erpnext.com" \
	//	target="_blank">'+__('User Forum')+'</a></li>').insertBefore($help_menu);
	//$('<li><a href="https://github.com/frappe/erpnext/issues" \
	//	target="_blank">'+__('Report an Issue')+'</a></li>').insertBefore($help_menu);

});
