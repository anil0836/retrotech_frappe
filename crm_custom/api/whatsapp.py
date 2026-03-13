import frappe

@frappe.whitelist(allow_guest=True)
def whatsapp_webhook():
    frappe.log_error("WEBHOOK HIT", "WHATSAPP")
    return {"status": "ok"}
