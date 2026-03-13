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

# Main duplicate check function
def check_salesforce_lead(email=None, phone=None, mobile=None, secondary_email=None):
    phone = clean_number(phone)
    mobile = clean_number(mobile)

    conditions = []

    if email:
        conditions.append(f"Email = '{email}'")
    if phone:
        conditions.append(f"Phone LIKE '%{phone}%'")
    if mobile:
        conditions.append(f"MobilePhone LIKE '%{mobile}%'")
    if secondary_email:
        conditions.append(f"Secondary_Email__c = '{secondary_email}'")

    if not conditions:
        return False

    where_clause = " OR ".join(conditions)

    # Check Lead object
    if query_salesforce("Lead", where_clause):
        return True
    # Check Contact object
    if query_salesforce("Contact", where_clause):
        return True

    return False