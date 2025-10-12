document.addEventListener("DOMContentLoaded", () => {
    const tabs = document.querySelectorAll(".tab-item")

    tabs.forEach((tab, index) => {
        tab.addEventListener("click", () => {
            tabs.forEach(t => t.classList.remove("border-b-2", "border-green-500", "text-green-500"))
            tab.classList.add("border-b-2", "border-green-500", "text-green-500")
        })
    })
})