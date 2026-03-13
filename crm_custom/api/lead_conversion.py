import frappe

@frappe.whitelist()
def convert_lead_to_account(lead_name):
    lead = frappe.get_doc("Lead", lead_name)

    # 1. Approval check (values exactly as you want)
    if lead.approval_status != "Approved":
        frappe.throw("Only Approved leads can be converted")

    # 2. Prevent double conversion
    if lead.crm_account:
        frappe.throw("Lead already converted")

    # 3. Create CRM Account
    account = frappe.get_doc({
        "doctype": "CRMAccount",
        "account_name": lead.company_name or lead.lead_name,
        "status": "Active"
    })
    account.insert(ignore_permissions=True)

    # 4. Link Lead → Account (THIS is the conversion)
    lead.crm_account = account.name
    lead.save(ignore_permissions=True)

    frappe.db.commit()

    return {
        "account": account.name
    }

