document.addEventListener('DOMContentLoaded', () => {
    selectSort = document.getElementById('sort')
    if (!selectSort) return
    pageButtons = document.querySelectorAll('.page-btn')
    postContainer = document.getElementById('userPosts')
    const baseUrl = postContainer.dataset.url

    selectSort.addEventListener('change', async (e) => {
        sortOption = e.target.value

        const html = await getPostList(baseUrl, sortOption, 1)
        postContainer.innerHTML = html
    })

    postContainer.addEventListener('click', async (e) => {
        if (e.target.classList.contains('page-btn')) {
            const page = e.target.dataset.page;
            const sortOption = selectSort.value;
            const html = await getPostList(baseUrl, sortOption, page)
            postContainer.innerHTML = html
            document.getElementById('profile-tabs').scrollIntoView({ behavior: 'smooth' });
        }
    });
})


async function getPostList(baseUrl, sortOption, page) {
    const response = await fetch(`${baseUrl}?sort=${sortOption}&page=${page}`)
    if (!response.ok) {
        text = await response.text()
        alert('An error occurred: ' + text)
        return
    }
    const html = await response.text()
    return html
}