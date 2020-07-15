//frappe.provide("solubis_brand.setup");

frappe.setup.on("before_load", function () {
	frappe.setup.remove_slide('domain');
	frappe.setup.remove_slide('user');
	//erpnext.setup.slides_settings.map(frappe.setup.add_slide);
});
/*frappe.setup.on("onload", function () {
	frappe.setup.domains="Retail"
	
});*/

frappe.pages['setup-wizard'].on_page_load = function(wrapper) {
	frappe.setup.domains="Retail"
};