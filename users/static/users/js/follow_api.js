export async function follow(url, csrfToken, profile_id) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            profile_id: profile_id,
        })
    })

    if (response.redirected) {
        const redirectUrl = response.url
        if (redirectUrl.includes('login')) {
            alert('You need to be logged in to comment. Redirecting to login...')
            window.location.href = redirectUrl
            return
        }
    }

    if (!response.ok) {
        text = await response.text()
        alert('An error occurred: ' + text)
        return
    }

    const result = await response.json()

    if (result.status == 'success') {
        return true
    }

    return false
}