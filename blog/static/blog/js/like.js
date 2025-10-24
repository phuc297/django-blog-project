document.querySelector("#sticky-bar #like").addEventListener("click", async (e) => {
    e.preventDefault()
    const likeButton = document.querySelector("#sticky-bar #like");
    const likeCountElem = document.querySelector("#sticky-bar p.text-xl");
    form = document.getElementById('commentForm')
    csrftoken = form.querySelector('[name=csrfmiddlewaretoken]').value
    post_id = form.querySelector('[name=post_id]').value
    const url = '/like/'

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": 'application/json',
        },
        body: JSON.stringify({
                post_id: post_id,
        }),
    })

    if (response.redirected) {
        const redirectUrl = response.url
        if (redirectUrl.includes('login')) {
            alert('You need to be logged in to comment. Redirecting to login...')
            window.location.href = redirectUrl
            return
        }
    }

    const contentType = response.headers.get('Content-Type')
    if (!contentType || !contentType.includes('application/json')) {
        console.error('Expected JSON, but received: ', response)
        alert('Unexpected response format. Please try again.')
        return
    }

    if (!response.ok) {
        text = await response.text()
        alert('An error occurred: ' + text)
        return
    }

    const result = await response.json()

    if (result.status == 'success') {
       //TODO code here
       likeCountElem.textContent = result.like_count;
        if (result.liked) {
            likeButton.classList.add("text-green-500", "border-green-500");
        } else {
            likeButton.classList.remove("text-green-500", "border-green-500");
        }
    } else {
        console.error(result.error)
    }
})