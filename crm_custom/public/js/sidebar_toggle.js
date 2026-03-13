frappe.ready(function () {
    if (!$('.sidebar-toggle').length) {
        $('<button class="sidebar-toggle">☰</button>')
            .prependTo('.navbar')
            .css({
                marginRight: '15px',
                background: 'transparent',
                border: 'none',
                color: 'white',
                fontSize: '20px',
                cursor: 'pointer'
            })
            .click(function () {
                $('.layout-side-section').toggle();
            });
    }
});
