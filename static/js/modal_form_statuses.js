document.body.addEventListener('htmx:afterRequest', function (event) {
    const modalEl = document.getElementById('formSourceModal');
    const successToastEl = document.getElementById('successToast');
    const errorToastEl = document.getElementById('errorToast');

    if (event.detail.xhr.status === 201) {
        const modalInstance = bootstrap.Modal.getInstance(modalEl);
        modalInstance.hide();

        const successToast = new bootstrap.Toast(successToastEl);
        successToast.show();
    } else if (event.detail.xhr.status === 400) {
        const errorToast = new bootstrap.Toast(errorToastEl);
        errorToast.show();
    }
});
