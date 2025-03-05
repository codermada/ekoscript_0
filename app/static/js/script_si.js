function deleteSupitem(supitem_id, story_id) {
    let confirmed = window.confirm('Are you sure you want to delete this supitem?');
    if (confirmed) {
        fetch(`/supitem/delete-supitem`, {
        method: "POST",
        body: JSON.stringify({supitem_id: supitem_id}) 
        }).then((_res)=> {
            window.location.href = `/supitem/?id=${story_id}`;
        })
    }
    
}

const updateBtn = document.querySelector("#update");
updateBtn.addEventListener("click", () => {
    document.getElementById("light_si").style.display = "block";
    document.getElementById("faded_si").style.display = "block";
})