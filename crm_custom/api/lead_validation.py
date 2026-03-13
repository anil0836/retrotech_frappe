import frappe
from crm_custom.integration.salesforce_api import check_salesforce_lead


def validate_salesforce_duplicate(doc, method):

    exists = check_salesforce_lead(
        email=doc.email_id,
        phone=doc.phone,
        mobile=doc.mobile_no,
        secondary_email=doc.get("secondary_email")
    )

    if exists:
        frappe.msgprint("❌ Lead already exists in Salesforce (Lead or Contact).",
                         indicator="red",
                         title="Duplicate Lead")
        frappe.validated = False






     