import frappe
import requests
import json

WHATSAPP_ACCESS_TOKEN = "EAAeBDMIXZAgsBQpWVh7Pz8sGbbBiUwO9C2hwhNZCuGe2YnYdoYKLdYNh3AKaMOinJpQ0NgvlqkcFSL6PIVvZAA7eY0PVrcVZAsZCJIkFW8VvEV1egLyATiRSIyDKjZCiUSuLjDTu3ZClroLZCUN9Sz41kByHTSeJNX4o5FzuryAjXPH8ALhBaoT4ka5MdEnc7rAtdofcb8gWGvl15ZBZC1eXmsfy51cD6OV9LAZALuNUTHoJzcQ7k6VgUigMnsfoIbbdJoCSvU1tqlZAg5Tw7l8kp4Uy"
PHONE_NUMBER_ID = "1001416176386921"
GRAPH_API_VERSION = "v22.0"


@frappe.whitelist(allow_guest=True)
def send_whatsapp_message(phone, message):
    """
    Send WhatsApp message using Meta Cloud API
    """

    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {
            "body": message
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    # Log response for debugging
    frappe.log_error(
        title="WHATSAPP SEND RESPONSE",
        message=response.text
    )

    if response.status_code not in (200, 201):
        frappe.throw("WhatsApp message failed")

    return response.json()
