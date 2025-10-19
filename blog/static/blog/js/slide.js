(() => {
    const slides = document.querySelector('.slides')
    const totalSlides = slides.children.length
    let index = 0

    document.getElementById('nextBtn').addEventListener('click', () => {
        index = (index + 1) % totalSlides
        updateSlide()
    })

    document.getElementById('prevBtn').addEventListener('click', () => {
        index = (index - 1 + totalSlides) % totalSlides
        updateSlide()
    })

    function updateSlide() {
        slides.style.transform = `translateX(-${index * 100}%)`
    }
})();