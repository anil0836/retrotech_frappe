frappe.ui.form.on('*', {
    refresh(frm) {
        if (!$('.lightning-enhanced').length) {
            $('.page-head').addClass('lightning-enhanced');
        }
    }
});
