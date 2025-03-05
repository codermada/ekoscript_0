function deleteChapter(chapter_id, story_id) {
    let confirmed = window.confirm('Are you sure you want to delete this chapter?');
    if (confirmed) {
        fetch(`/chapter/delete-chapter`, {
        method: "POST",
        body: JSON.stringify({chapter_id: chapter_id}) 
        }).then((_res)=> {
            window.location.href = `/chapter/?id=${story_id}`;
        })
    }
    
}

const updateBtn = document.querySelector("#update");
updateBtn.addEventListener("click", () => {
    document.getElementById("light_chapter").style.display = "block";
    document.getElementById("faded_chapter").style.display = "block";
})

