document.addEventListener('htmx:afterSwap', function (evt) {
    if (evt.target.closest('.dropdown')) {
        const dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'))
        dropdownElementList.map(function (dropdownToggleEl) {
            new bootstrap.Dropdown(dropdownToggleEl)
        })
    }
});

