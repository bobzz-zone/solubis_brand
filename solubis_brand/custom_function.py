from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.frappeclient import FrappeClient
from frappe.core.doctype.data_import.data_import import import_doc, export_json

@frappe.whitelist()
def disable_signup_website():
	# role_baru = frappe.get_doc({
	# 	"doctype":"Role",
	# 	"role_name": "BiSetup Wizard"
	# })
	# role_baru.flags.ignore_permissions = True
	# role_baru.insert()
	ws = frappe.get_single("Website Settings")
	ws.disable_signup = 1
	ws.top_bar_items = []
	ws.flags.ignore_permissions = True
	ws.save()

@frappe.whitelist()
def create_user_baru(fullname_user, email, password,plan):
	# custom andy System Manager user selain administrator
	setting = frappe.get_single("Additional Settings")
	user = frappe.get_doc({
		"doctype":"User",
		"email" : setting.email_sender,
		"first_name" : setting.url,
		"last_name" :"contact",

		"enabled" : 1,
		"send_welcome_email" : 0,
		"thread_notify" : 0,
		"new_password" : "Majuterus234@",
		"block_modules" : [
			
		],
		"roles" : [
			{"role" : "System Manager"},
			# {"role" : "Website Manager"},
			# {"role" : "Accounts Manager"},
			# {"role" : "Accounts User"},
			# {"role" : "HR Manager"},
			# {"role" : "HR User"},
			# {"role" : "Item Manager"},
			# {"role" : "Manufacturing Manager"},
			# {"role" : "Manufacturing User"},
			# {"role" : "Purchase Manager"},
			# {"role" : "Purchase User"},
			# {"role" : "Projects User"},
			# {"role" : "Projects Manager"},
			# {"role" : "Sales Manager"},
			# {"role" : "Sales User"},
			# {"role" : "Stock Manager"},
			# {"role" : "Stock User"},
			# {"role" : "Sales Master Manager"},
			# {"role" : "Report Manager"},
			# {"role" : "All"},
			# {"role" : "Purchase Master Manager"}
		],
	})
	user.flags.ignore_permissions = True
	user.insert()

	user = frappe.get_doc({
		"doctype":"User",
		"email" : email,
		"first_name" : fullname_user,

		"enabled" : 1,
		"send_welcome_email" : 0,
		"thread_notify" : 0,
		"new_password" : password,
		"block_modules" : [
			
		],
		"roles" : [
			{"role":plan}
			# {"role" : "System Manager"},
			# {"role" : "Website Manager"},
			# {"role" : "Accounts Manager"},
			# {"role" : "Accounts User"},
			# {"role" : "HR Manager"},
			# {"role" : "HR User"},
			# {"role" : "Item Manager"},
			# {"role" : "Manufacturing Manager"},
			# {"role" : "Manufacturing User"},
			# {"role" : "Purchase Manager"},
			# {"role" : "Purchase User"},
			# {"role" : "Projects User"},
			# {"role" : "Projects Manager"},
			# {"role" : "Sales Manager"},
			# {"role" : "Sales User"},
			# {"role" : "Stock Manager"},
			# {"role" : "Stock User"},
			# {"role" : "Sales Master Manager"},
			# {"role" : "Report Manager"},
			# {"role" : "All"},
			# {"role" : "Purchase Master Manager"}
		],
	})
	user.flags.ignore_permissions = True
	user.insert()

def import_fixtures():
	# import_doc(frappe.get_app_path("my_account", "fixtures", "custom_field.json"), ignore_links=False, overwrite=True)
	import_doc(frappe.get_app_path("my_account", "fixtures", "property_setter.json"), ignore_links=False, overwrite=True)
	import_doc(frappe.get_app_path("my_account", "fixtures", "custom_docperm.json"), ignore_links=False, overwrite=True)
	import_doc(frappe.get_app_path("my_account", "fixtures", "role.json"), ignore_links=False, overwrite=True)
	import_doc(frappe.get_app_path("my_account", "fixtures", "setup_wizard_system_manager.json"), ignore_links=False, overwrite=True)