// Force exact timestamp instead of relative time in Frappe v15

frappe.after_ajax(() => {

    if (!frappe.ui.form || !frappe.ui.form.Timeline) return;

    const OriginalTimeline = frappe.ui.form.Timeline;

    frappe.ui.form.Timeline = class CustomTimeline extends OriginalTimeline {
        render_timeline_items() {
            super.render_timeline_items();

            setTimeout(() => {
                document.querySelectorAll(".frappe-timestamp").forEach(el => {
                    const dt = el.getAttribute("data-timestamp");
                    if (dt) {
                        el.innerText = frappe.datetime.str_to_user(dt);
                    }
                });
            }, 300);
        }
    };

});
