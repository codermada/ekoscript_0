function deleteChapter(panel_id, chapter_id) {
    let confirmed = window.confirm('Are you sure you want to delete this panel?');
    if (confirmed) {
        fetch(`/panel/delete-panel`, {
        method: "POST",
        body: JSON.stringify({panel_id: panel_id}) 
        }).then((_res)=> {
            window.location.href = `/panel/?id=${chapter_id}`;
        })
    }
    
}

const updateBtn = document.querySelector("#update");
updateBtn.addEventListener("click", () => {
    document.getElementById("light_p").style.display = "block";
    document.getElementById("faded_p").style.display = "block";
})