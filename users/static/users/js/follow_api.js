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
    }

    )
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