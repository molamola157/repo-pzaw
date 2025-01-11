function react(postId, action) {
    fetch(`/polls/${postId}/${action}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'post_id': postId,
            'action': action
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    });
}
