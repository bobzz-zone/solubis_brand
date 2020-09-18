from __future__ import unicode_literals
from frappe.model.document import Document
from frappe import _
import json
import frappe
from six import string_types
from erpnext.stock.get_item_details import get_item_details
from erpnext.accounts.doctype.pricing_rule.pricing_rule import apply_pricing_rule
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
def apply_pl(customer,customer_group,territory,currency,price_list,campaign,item_list):
	price_list = get_default_price_list(customer)
	company = get_default_company()
	item_final = []
	if isinstance(item_list, string_types):
		item_list = json.loads(item_list)
	return item_list
	for d in item_list:
		temp ={
			"item_code": d.item_code,
			"item_group": d.item_group,
			"brand": d.brand,
			"qty": d.qty,
			"stock_qty": d.qty,
			"uom": d.uom,
			"stock_uom": d.uom,
			"pricing_rules": d.pricing_rules,
			"warehouse": get_default_warehouse(d.warehouse),
			"serial_no": "",
			"price_list_rate": d.price_list_rate,
			"conversion_factor": 1.0
		}
		item_final.append(temp);
	args = {
		"customer": customer,
		"items":item_final,
		"customer_group": customer_group,
		"territory": territory,
		"currency": currency,
		"conversion_rate": 1,
		"price_list": price_list,
		"price_list_currency": currency,
		"plc_conversion_rate": 1,
		"company": company,
		"transaction_date": frappe.utils.today(),
		"campaign": campaign,
		"sales_partner": "",
		"ignore_pricing_rule": 0,
		"doctype": "Sales Invoice",
		"name": "",
		"is_return": 0,
		"update_stock": 0,
		"conversion_factor": 1,
		"pos_profile": "",
		"coupon_code": ""
	}
	return apply_pricing_rule(args)
@frappe.whitelist()
def get_item_price(customer="Karya Jaya, CV.",warehouse="Stores - T",item_code="",qty=1):
	warehouse = get_default_warehouse(warehouse)
	price_list = get_default_price_list(customer)
	company = get_default_company()

	docsargs = {
		"item_code": item_code,
		"warehouse": warehouse,
		"customer": customer,
		"currency": "IDR",
		"price_list": price_list,
		"price_list_currency": "IDR",
		"plc_conversion_rate": 1,
		"company": company,
		"transaction_date": frappe.utils.today(),
		"ignore_pricing_rule": 0,
		"qty":qty,
		"doctype": "Sales Invoice"
	}
	return get_item_details(docsargs)
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
	company = frappe.get_doc("Company",get_default_company())
	return frappe.db.sql("""select c.name , c.customer_group , c.territory , c.customer_name , c.mobile_no , c.primary_address ,c.email_id, IFNULL(d.account,"{2}") as default_piutang from `tabCustomer` c left join `tabParty Account` d on d.parent=c.name and d.company="{1}" where c.customer_name like "{0}" or c.name like "{0}" or c.mobile_no like "{0}" or c.primary_address like "{0}" """.format(keyword,company.name,company.default_receivable_account), as_dict=1)
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
			if customer[0]["default_price_list"] and customer[0]["default_price_list"]!="":
				return customer[0]["default_price_list"] 
	
	return default_price_list
