import { follow } from '/static/users/js/follow_api.js';

document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById('followButton')
    if (!button) return

    button.addEventListener("click", async (e) => {
        const url = button.dataset.url
        const profile_id = button.dataset.profileId

        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        const success = await follow(url, csrfToken, profile_id)
        if (success) {
            button.classList.toggle("border-green-500");
            button.classList.toggle("text-green-500");
            button.classList.toggle("border-gray-500");
            button.classList.toggle("text-gray-500");
            button.textContent = button.textContent === 'Theo dõi' ? 'Đang theo dõi' : 'Theo dõi'
        }
    })
})


