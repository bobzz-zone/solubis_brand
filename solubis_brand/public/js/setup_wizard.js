//frappe.provide("solubis_brand.setup");

frappe.setup.on("before_load", function () {
	frappe.setup.remove_slide('domain');
	frappe.setup.remove_slide('user');
	//erpnext.setup.slides_settings.map(frappe.setup.add_slide);
});
frappe.setup.on("after_load", function () {
	frappe.setup.domains="Retail"
	frappe.wizard.values['domains']="Retail"
	
});
