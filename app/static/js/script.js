function deleteStory(story_id) {
    let confirmed = window.confirm('Are you sure you want to delete this story?');
    if (confirmed) {
        fetch(`/delete-story`, {
        method: "POST",
        body: JSON.stringify({story_id: story_id}) 
        }).then((_res)=> {
            window.location.href = '/';
        })
    }
    
}

const updateBtn = document.querySelector("#update");
updateBtn.addEventListener("click", () => {
    document.getElementById("light_story").style.display = "block";
    document.getElementById("faded_story").style.display = "block";
})

