import frappe


def after_save(doc, method):

    # find lead using name
    lead = frappe.db.get_all(
        "Lead",
        filters={
            "lead_name": doc.account_name
        },
        fields=[
            "lead_name",
            "email_id",
            "mobile_no",
            "phone",
            "job_title"
        ],
        order_by="modified desc",
        limit=1
    )

    lead = lead[0] if lead else None

    full_name = doc.account_name
    email = None
    phone = None
    mobile = None
    designation = None

    if lead:
        full_name = lead.get("lead_name")
        email = lead.get("email_id")
        phone = lead.get("phone")
        mobile = lead.get("mobile_no")
        designation = lead.get("job_title")

    # check already exists
    exists = frappe.db.exists(
        "CRM Contact",
        {
            "crm_account": doc.name
        }
    )

    if exists:
        return

    # create CRM Contact
    contact = frappe.get_doc({
        "doctype": "CRM Contact",
        "crm_account": doc.name,
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "mobile": mobile,
        "designation": designation
    })

    contact.insert(ignore_permissions=True)
