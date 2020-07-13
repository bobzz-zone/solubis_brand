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
			{"role" : "System Manager"},
			{"role" : plan},
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
@frappe.whitelist()
def disable_other_roles(plan):
	frappe.db.sql("update `tabRole` set disabled = 1 where name not in ('Administrator','System Manager','All','Guest','{}') ".format(plan))
	frappe.db.commit()

def import_fixtures():
	# import_doc(frappe.get_app_path("my_account", "fixtures", "custom_field.json"), ignore_links=False, overwrite=True)
	import_doc(frappe.get_app_path("my_account", "fixtures", "property_setter.json"), ignore_links=False, overwrite=True)
	import_doc(frappe.get_app_path("my_account", "fixtures", "custom_docperm.json"), ignore_links=False, overwrite=True)
	import_doc(frappe.get_app_path("my_account", "fixtures", "role.json"), ignore_links=False, overwrite=True)
	import_doc(frappe.get_app_path("my_account", "fixtures", "setup_wizard_system_manager.json"), ignore_links=False, overwrite=True)