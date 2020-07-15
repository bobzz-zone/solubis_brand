# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "solubis_brand"
app_title = "Solubis Brand"
app_publisher = "bobzz.zone@gmail.com"
app_description = "For Styling"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "bobzz.zone@gmail.com"
app_license = "MIT"
app_logo_url ="/assets/solubis_brand/images/logo_icon.png"
website_context = {
	"favicon": 	"/assets/solubis_brand/images/logo_icon.png",
	"splash_image": "/assets/solubis_brand/images/logo.png"
}
# Includes in <head>
# ------------------
app_include_css = "assets/css/styling.min.css"
app_include_js = "assets/js/styling.min.js"
# include js, css files in header of desk.html
# app_include_css = "/assets/solubis_brand/css/solubis_brand.css"
# app_include_js = "/assets/solubis_brand/js/solubis_brand.js"

# include js, css files in header of web template
# web_include_css = "/assets/solubis_brand/css/solubis_brand.css"
# web_include_js = "/assets/solubis_brand/js/solubis_brand.js"
setup_wizard_requires = "assets/solubis_brand/js/setup_wizard.js"
#setup_wizard_stages = "solubis_brand.setup_wizard.get_setup_stages"
# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "solubis_brand.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "solubis_brand.install.before_install"
after_install = "solubis_brand.custom_function.after_install"
on_login="solubis_brand.custom_function.login_block"
# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "solubis_brand.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"User": {
		"validate": "solubis_brand.custom_function.validate_user_quota",
		"before_insert": "solubis_brand.custom_function.set_block_module"
		# "on_submit" : my_account.doctype.sync_server_settings.create_new_user
	}
}

# on_session_creation =[
# 	"solubis_brand.custom_function.login_block"
# ]
# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"solubis_brand.tasks.all"
# 	],
# 	"daily": [
# 		"solubis_brand.tasks.daily"
# 	],
# 	"hourly": [
# 		"solubis_brand.tasks.hourly"
# 	],
# 	"weekly": [
# 		"solubis_brand.tasks.weekly"
# 	]
# 	"monthly": [
# 		"solubis_brand.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "solubis_brand.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "solubis_brand.event.get_events"
# }

