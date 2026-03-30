import requests
import frappe
import re

# Salesforce Access Details
ACCESS_TOKEN = frappe.conf.get("salesforce_access_token")
INSTANCE_URL = frappe.conf.get("salesforce_instance_url")

# Remove spaces, +, -, etc. from phone numbers
def clean_number(number):
    if not number:
        return None
    return re.sub(r"\D", "", number)

# Query Salesforce Object
def query_salesforce(object_name, where_clause):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    query = f"""
        SELECT Id, Name, Email, Phone, MobilePhone
        FROM {object_name}
        WHERE {where_clause}
    """

    url = f"{INSTANCE_URL}/services/data/v58.0/query"
    response = requests.get(url, headers=headers, params={"q": query})

    if response.status_code != 200:
        frappe.log_error(response.text, "Salesforce Query Failed")
        return False

    data = response.json()
    return data.get("totalSize", 0) > 0


# Main duplicate check function (UPDATED)
def check_salesforce_lead(email=None, phone=None, mobile=None, secondary_email=None):
    phone = clean_number(phone)
    mobile = clean_number(mobile)

    duplicates = {
        "email": False,
        "phone": False,
        "mobile": False,
        "secondary_email": False
    }

    # 🔹 Email check
    if email:
        if query_salesforce("Lead", f"Email = '{email}'") or \
           query_salesforce("Contact", f"Email = '{email}'"):
            duplicates["email"] = True

    # 🔹 Phone check
    if phone:
        if query_salesforce("Lead", f"Phone LIKE '%{phone}%'") or \
           query_salesforce("Contact", f"Phone LIKE '%{phone}%'"):
            duplicates["phone"] = True

    # 🔹 Mobile check
    if mobile:
        if query_salesforce("Lead", f"MobilePhone LIKE '%{mobile}%'") or \
           query_salesforce("Contact", f"MobilePhone LIKE '%{mobile}%'"):
            duplicates["mobile"] = True

    # 🔹 Secondary Email check
    if secondary_email:
        if query_salesforce("Lead", f"Secondary_Email__c = '{secondary_email}'") or \
           query_salesforce("Contact", f"Secondary_Email__c = '{secondary_email}'"):
            duplicates["secondary_email"] = True

    return duplicates
