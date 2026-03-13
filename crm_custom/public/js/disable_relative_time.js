frappe.ready(function () {

    // Override global formatter once after boot
    frappe.after_ajax(function () {

        document.querySelectorAll(".frappe-timestamp").forEach(function (el) {
            let dt = el.getAttribute("data-timestamp");
            if (dt) {
                el.innerText = frappe.datetime.str_to_user(dt);
                el.classList.remove("frappe-timestamp");
            }
        });

    });

});
