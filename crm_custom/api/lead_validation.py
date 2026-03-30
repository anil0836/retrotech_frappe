import frappe
from crm_custom.integration.salesforce_api import check_salesforce_lead


def validate_salesforce_duplicate(doc, method):

    result = check_salesforce_lead(
        email=doc.email_id,
        phone=doc.phone,
        mobile=doc.mobile_no,
        secondary_email=doc.get("secondary_email")
    )

    messages = []

    if result["email"]:
        messages.append("Email already exists in Salesforce")

    if result["phone"]:
        messages.append("Phone already exists in Salesforce")

    if result["mobile"]:
        messages.append("Mobile already exists in Salesforce")

    if result["secondary_email"]:
        messages.append("Secondary Email already exists in Salesforce")

    # ✅ Create exists flag
    exists = any(result.values())

    # ✅ Option 1: Detailed error (recommended)
    if messages:
        frappe.throw("❌ Duplicate Found:\n" + "\n".join(messages))

    # ✅ Option 2: Generic error (your requirement)
    if exists:
        frappe.throw("Lead already exists in Salesforce (Lead or Contact)")
