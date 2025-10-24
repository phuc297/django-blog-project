(function initCommentForm() {
    form = document.getElementById('commentForm')
    form.addEventListener('submit', async (e) => {
        e.preventDefault()
        csrftoken = form.querySelector('[name=csrfmiddlewaretoken]').value
        post_id = form.querySelector('[name=post_id]').value
        content = form.querySelector('[name=content]').value
        const response = await fetch(form.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                post_id: post_id,
                content: content
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
            const newCommentDiv = `<div class="bg-white border border-gray-200 rounded-lg my-3 p-4">
              <div class="flex items-center">
                <img class="w-12 h-12 rounded-full" src="${result.avatar_url}" alt="User" />
                <p class="hover:underline cursor-pointer">${result.user}</p>
              </div>
              <p class="text-gray-500 text-sm mb-1">Posted ${result.created_at}</p>
              <p class="">${result.content}</p>
            </div>`

            const cmtElems = document.querySelectorAll("#commentCount");
            cmtElems.forEach(cmtElem => {
                const currentText = cmtElem.textContent.trim();
                const currentCount = parseInt(currentText)
                const newCount = currentCount + 1;
                cmtElem.textContent = `${newCount}`;
            });

            document.getElementById('commentList').insertAdjacentHTML('afterbegin', newCommentDiv)
            form.querySelector('[name=content]').value = ''
        } else {
            console.error(result.error)
        }
    })
})();