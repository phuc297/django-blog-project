(function initSocialBar() {
    document.addEventListener('DOMContentLoaded', function () {
        const stickyBar = document.getElementById('sticky-bar')

        const triggerElement = document.querySelector('article')

        const footerOffset = 500

        function toggleStickyBar() {
            const triggerTop = triggerElement.getBoundingClientRect().top

            const triggerBottom = triggerElement.getBoundingClientRect().bottom

            const scrollBottom = window.innerHeight + window.scrollY

            const documentHeight = document.body.offsetHeight

            const shouldShow = triggerTop < window.innerHeight * 0.425 && triggerBottom > 100

            const shouldHide = scrollBottom + footerOffset >= documentHeight

            if (shouldShow && !shouldHide) {
                stickyBar.classList.remove('opacity-0', 'pointer-events-none')
            } else {
                stickyBar.classList.add('opacity-0', 'pointer-events-none')
            }
        }

        window.addEventListener('scroll', toggleStickyBar)

        toggleStickyBar()
    })
})();