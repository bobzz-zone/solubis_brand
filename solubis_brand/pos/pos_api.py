from __future__ import unicode_literals
from frappe.model.document import Document
from frappe import _
import json
import frappe
from erpnext.stock.get_item_details import get_item_details
from frappe.utils import cint, flt
class pos_api(Document):
	pass
@frappe.whitelist()
def get_item_list(customer="Karya Jaya, CV.",warehouse="Stores - T",keyword="%",item_group="All",page=1,limit=20):
	page=cint(page)
	limit=cint(limit)
	keyword="%{}%".format(keyword)
	filters={"variant_of" : '' ,"is_sales_item":1}
	if item_group and item_group!="All":
		filters["item_group"]=item_group
	list_item = frappe.get_all("Item",fields=["item_code","item_name","item_group","brand","description","image","stock_uom","has_variants"],filters=filters,or_filters={"item_code":["like",keyword],"item_name":["like",keyword],"description":["like",keyword]},limit_start=(page-1)*limit,limit_page_length=limit)
	if len(list_item)>0:
		result=[]
		today = frappe.utils.today()
		for row in list_item:
			result.append(master_get_item_details(
				warehouse = warehouse,
				customer = customer,
				transaction_date = today,
				doc_item = row))
		return result
	else:
		return {"Error":"No Item Found"}
@frappe.whitelist()
def get_item_by_barcode(barcode,customer,warehouse):
	pass
@frappe.whitelist()
def test():
	print("test")

@frappe.whitelist()
def get_item_variant(item,customer,warehouse):
	list_item = frappe.get_all("Item",fields=["item_code","item_name","item_group","brand","description","image","stock_uom"],filters={"variant_of":item,"is_sales_item":1})
	if len(list_item)>0:
		result=[]
		today = frappe.utils.today()
		for row in list_item:
			row.attributes=frappe.get_all("Item Variant Attribute",fields=["attribute","attribute_value"],filters={"parent":row.item_code})
			result.append(master_get_item_details(
				warehouse = warehouse,
				customer = customer,
				transaction_date = today,
				doc_item = row))
		return result
	else:
		return {"Error":"Variant Not Found"}

@frappe.whitelist()
def get_pos_profile(user):
	profile=frappe.db.sql("""select parent from `tabPOS Profile User` where `default`=1 and user="{}" """.format(user),as_list=1)
	if len(profile)>0:
		return frappe.get_doc("POS Profile",profile[0][0])
	else:
		return {"Error":"Default Profile Not Found"}
@frappe.whitelist()
def get_customer(keyword):
	keyword="%{}%".format(keyword)
	return frappe.db.sql("""select name , customer_group , territory , customer_name , mobile_no , primary_address ,email_id from `tabCustomer` where customer_name like "{0}" or name like "{0}" or mobile_no like "{0}" or primary_address like "{0}" """.format(keyword), as_dict=1)
def master_get_item_details(warehouse,customer, transaction_date,doc_item):
	warehouse = get_default_warehouse(warehouse)
	price_list = get_default_price_list(customer)
	company = get_default_company()

	docsargs = {
		"item_code": doc_item.item_code,
		"warehouse": warehouse,
		"customer": customer,
		"currency": "IDR",
		"price_list": price_list,
		"price_list_currency": "IDR",
		"plc_conversion_rate": 1,
		"company": company,
		"transaction_date": transaction_date,
		"ignore_pricing_rule": 0,
		"doctype": "Sales Invoice"
	}
	if doc_item.has_variants==1:
		list_item = frappe.db.sql("""select i.item_code from `tabItem` i 
			left join `tabItem Price` ip on ip.item_code=i.item_code and ip.price_list="{}"
			where i.variant_of="{}" and i.disabled=0
			order by ip.price_list_rate asc
			limit 0,1
			""".format(price_list,doc_item.item_code),as_list=True)
		if len(list_item)==0:
			return {"item_detail" : doc_item}
		docsargs["item_code"] = list_item[0][0]
	doc_item.price_detail = get_item_details(docsargs)
	return {"item_detail":doc_item}

def get_default_company():
	default_company = frappe.get_value("Global Defaults","Global Defaults","default_company")
	if default_company:
		return default_company
	else:
		fg_company = frappe.get_list("Company",fields="name")
		if len(fg_company) > 0:
			return fg_company[0]["name"]

def get_default_warehouse(warehouse=""):
	if warehouse:
		return warehouse
	else:
		default_warehouse = frappe.get_value("Stock Settings","Stock Settings","default_warehouse")
		return default_warehouse

def get_default_price_list( customer=""):
	default_price_list = frappe.get_value("Selling Settings","Selling Settings","selling_price_list")
	if customer and customer!="":
		customer = frappe.get_all("Customer", fields= "*", filters=[["name","=",customer]])
		if len(customer) > 0:
			if customer[0]["default_price_list"]:
				return customer[0]["default_price_list"] 
	
	return default_price_list
