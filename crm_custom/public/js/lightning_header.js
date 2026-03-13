frappe.ui.form.on('*', {
    refresh(frm) {
        setTimeout(() => {
            if (!$('.lightning-enhanced').length) {
                $('.page-head').addClass('lightning-enhanced');

                // Add blue left border like Salesforce
                $('.page-head').css({
                    borderLeft: '6px solid #0176d3'
                });
            }
        }, 200);
    }
});
