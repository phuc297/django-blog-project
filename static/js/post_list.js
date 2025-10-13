document.querySelectorAll("#divSort .sortRadio").forEach(radio => {
    radio.addEventListener("change", (e) => {
        e.preventDefault();
        radio.form.submit();
    });
});