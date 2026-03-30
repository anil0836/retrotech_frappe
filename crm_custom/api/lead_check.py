import frappe


@frappe.whitelist(allow_guest=True)
def check_lead_duplicate(email=None, mobile=None, phone=None, secondary_email=None):

    conditions = []

    if email:
        conditions.append(f"email_id = '{email}'")

    if secondary_email:
        conditions.append(f"secondary_email = '{secondary_email}'")

    if mobile:
        conditions.append(f"mobile_no = '{mobile}'")

    if phone:
        conditions.append(f"phone = '{phone}'")

    if not conditions:
        return {"duplicate": False}

    where_clause = " OR ".join(conditions)

    query = f"""
        SELECT name,email_id,mobile_no,phone
        FROM `tabLead`
        WHERE {where_clause}
        LIMIT 1
    """

    result = frappe.db.sql(query, as_dict=True)

    if result:
        return {
            "duplicate": True,
            "data": result
        }

    return {"duplicate": False}
