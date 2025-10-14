(() => {
    document.addEventListener("DOMContentLoaded", () => {
        document.querySelectorAll("#divSort .sortRadio").forEach(radio => {
            radio.addEventListener("change", (e) => {
                e.preventDefault();
                radio.form.submit();
            });
        });

        const toggleBtn = document.getElementById("toggleAccordionBtn");
        const divAccordion = document.getElementById("accordion");

        toggleBtn = document.getElementById("toggleAccordionBtn").addEventListener("click", () => {
            isHidden = divAccordion.classList.toggle("hidden")
            toggleBtn.textContent = isHidden ? "Hiện bộ lọc" : "Ẩn bộ lọc";
        })
    })
})();