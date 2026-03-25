import frappe

@frappe.whitelist()
def convert_lead_to_account(lead_name):
    lead = frappe.get_doc("Lead", lead_name)

    # 1. Approval check
    if lead.approval_status != "Approved":
        frappe.throw("Only Approved leads can be converted")

    # 2. Prevent double conversion
    if lead.crm_account:
        frappe.throw("Lead already converted")

    # 3. Create CRM Account (with contact data)
    account = frappe.get_doc({
        "doctype": "CRMAccount",
        "account_name": lead.company_name or lead.lead_name,
        "email": lead.email_id,      # Store email in account
        "phone": lead.phone,          # Store phone in account
        "mobile": lead.mobile_no,     # Store mobile in account
        "status": "Active"
    })
    account.insert(ignore_permissions=True)

    # 4. Create CRM Contact with unique name and ALL data
    contact_name = f"{lead.lead_name}-{account.name}"
    
    crm_contact = frappe.get_doc({
        "doctype": "CRM Contact",
        "name": contact_name,
        "crm_account": account.name,
        "full_name": lead.lead_name,
        "email": lead.email_id,        # CRITICAL: Map email_id to email
        "phone": lead.phone,           # CRITICAL: Map phone to phone
        "mobile": lead.mobile_no,      # CRITICAL: Map mobile_no to mobile
        "designation": lead.job_title
    })
    crm_contact.insert(ignore_permissions=True)

    # 5. Link Lead to Account
    lead.crm_account = account.name
    # DON'T change approval_status - keep as "Approved"
    lead.save(ignore_permissions=True)

    frappe.db.commit()

    return {
        "account": account.name,
        "account_name": account.account_name,
        "crm_contact": crm_contact.name,
        "contact_name": crm_contact.full_name,
        "email": crm_contact.email,
        "phone": crm_contact.phone,
        "mobile": crm_contact.mobile,
        "message": f"Successfully converted {lead.lead_name} to Account and Contact"
    }
