from __future__ import unicode_literals
from frappe.model.document import Document
from frappe import _
import json
import frappe
from frappe.utils.password import get_decrypted_password
from frappe.utils.password import check_password

@frappe.whitelist(allow_guest=True)
def validate_token(token):
	token = validate_token(post["token"])
	if token["data"] == 1:
		return {"description" : "User Valid", "valid" : 1}
	else:
		return {"description" : "User not Valid", "valid" : 0}

@frappe.whitelist(allow_guest=True)
def login_and_get_key(user,password):
	return get_api_key_with_password(post["user"],post["password"])

def create_or_update_secret_key(user):
	""" args: user"""
	check_exist = frappe.db.exists("User", user)
	if check_exist:
		user_doc = frappe.get_doc("User",user)
		if user_doc.api_key:
			api_secret_string = get_password("User",user,"api_secret")
			if api_secret_string: 
				token_string = "token " + str(user_doc.api_key)+":"+str(api_secret_string)
				return {"data":1, "description" : token_string, "user" : user_doc}
		else:
			from frappe.core.doctype.user.user import generate_keys
			frappe.set_user("Administrator")
			secret = generate_keys(user)
			user_doc = frappe.get_doc("User",user)
			token_string = "token " + str(user_doc.api_key)+":"+str(secret["api_secret"]) 
			return {"data":1, "description" : token_string}
	
	frappe.throw(_("User not found. Please check your data :)"))



def validate_token(token):
	if "token " in token and ":" in token:
		token = token.replace("token ","")
		token_api_access = token.split(":")
		fga_user = frappe.get_all("User",filters=[["api_key","=",token_api_access[0]]])
		if len(fga_user) > 0:
			api_secret_string = get_password("User",fga_user[0]["name"],"api_secret")
			if token_api_access[1] == api_secret_string:
				return {"data":1, "description" : "Token Valid"}
	else:
		frappe.throw("Invalid token. Please contact administrator.")
	
	return {"data":0, "description" : "Token Invalid"}

def get_api_key_with_password(user, password):
	pass_correct = validate_password(user,password)
	if pass_correct == False:
		frappe.throw("Invalid email or password.")
	else:
		response = create_or_update_secret_key(user)
		if response["data"] == 1:
			if frappe.db.exists("User",user):
				doc = frappe.get_doc("User",user)
				return {"user" : doc, "token" : response["description"]}
		else:
			frappe.throw(response["description"])
	
# STUB small function

def get_password(doctype,name,fieldname):
	'''
	Untuk mengambil password dari field Frappe yang bertipekan `password`
	'''
	d_password = get_decrypted_password(doctype, name, fieldname=fieldname, raise_exception=False)
	return d_password

def validate_password(user, password):
	try:
		check_password(user, password)
		return True
	except:
		return False