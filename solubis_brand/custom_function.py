from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.frappeclient import FrappeClient
from frappe.core.doctype.data_import.data_import import import_doc, export_json
import subprocess
from frappe.utils import cint, flt
import requests
import json

def after_install():
	subdomain = frappe.local.site.split(".")[0]
#	url = "https://reg.solubis.id/api/method/my_account.my_account.doctype.custom_method.get_site_data?subdomain={}".format(subdomain)
#	raw = requests.get(url).json()
#	data = raw['message']
	import_fixtures()
	disable_signup_website()
#	disable_other_roles(data['active_plan'])
#	create_user_baru(data['fullname'], data['user'], data['password'],data['active_plan'])
	frappe.db.commit()
#	requests.get("https://reg.solubis.id/api/method/my_account.custom_dns_api.send_mail_site_created?subdomuser={}&fullname={}&newsitename={}".format(data['user'],data['fullname'],frappe.local.site))


@frappe.whitelist()
def disable_signup_website():
	ws = frappe.get_single("Website Settings")
	ws.disable_signup = 1
	ws.top_bar_items = []
	ws.flags.ignore_permissions = True
	ws.save()
@frappe.whitelist()
def set_block_module(doc,method):
	if doc.name:
		doc.block_modules=[
			{"module" : "Integrations"},
			{"module" : "Social"},
			{"module" : "Assets"},
			{"module" : "CRM"},
			{"module" : "HR"},
			{"module" : "Marketplace"},
			{"module" : "Leaderboard"},
			{"module" : "Projects"},
			{"module" : "Support"},
			{"module" : "Quality Management"},
			{"module" : "Help"}
		]


@frappe.whitelist()
def login_block():
	subdomain = frappe.local.site.split(".")[0]
	url = "https://reg.solubis.id/api/method/my_account.my_account.doctype.custom_method.get_site_data?subdomain={}".format(subdomain)
	raw = requests.get(url).json()
	data = raw['message']
	if data['block'] and data['block']==1:
		frappe.throw("Login Block Due To Billing Unpaid , please kindly check or contact us..")


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
			{"module" : "Integrations"},
			{"module" : "Social"},
			{"module" : "Assets"},
			{"module" : "CRM"},
			{"module" : "HR"},
			{"module" : "Marketplace"},
			{"module" : "Leaderboard"},
			{"module" : "Projects"},
			{"module" : "Support"},
			{"module" : "Quality Management"},
			{"module" : "Help"},
			{"module" : "Website"}
		],
		"roles" : [
			{"role" : "System Manager"},
			#{"role" : plan},
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

@frappe.whitelist()
def get_enabled_users():
	return frappe.db.sql("""select CAST(COUNT(*) AS CHAR) from `tabUser`
		where enabled = 1 and name not in ("Administrator","Guest") """)[0][0]
@frappe.whitelist()
def validate_user_quota(doc,method):
	if doc.name in ["Administrator","Guest"]:
		return
	is_created = 1
	try:
		subdomain = frappe.local.site.split(".")[0]
	except:
		frappe.throw("Domain not found")
	subdomain = frappe.local.site.split(".")[0]
	url = "https://reg.solubis.id/api/method/my_account.my_account.doctype.custom_method.get_site_data?subdomain={}".format(subdomain)
	raw = requests.get(url).json()
	data = raw['message']
	quota = flt(data['quota'])
	enabled_users = get_enabled_users()
		# print("enabled = {}".format(enabled_users))
	# print("quota = {}".format(quota))
	if flt(quota) < flt(enabled_users):
		frappe.throw("Max enabled users reached for {} ({}/{})".format(frappe.local.site,flt(quota),flt(enabled_users)))
	
