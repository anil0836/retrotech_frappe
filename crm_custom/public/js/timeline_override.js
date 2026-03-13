frappe.ready(function () {

    // Override global relative time formatter (v15 compatible)
    if (frappe.utils && frappe.utils.formatters) {

        frappe.utils.formatters.format_relative = function (value) {
            return frappe.datetime.str_to_user(value);
        };

    }

});
