function deleteSupcharacter(supcharacter_id, story_id) {
    let confirmed = window.confirm('Are you sure you want to delete this supcharacter?');
    if (confirmed) {
        fetch(`/supcharacter/delete-supcharacter`, {
        method: "POST",
        body: JSON.stringify({supcharacter_id: supcharacter_id}) 
        }).then((_res)=> {
            window.location.href = `/supcharacter/?id=${story_id}`;
        })
    }
    
}

const updateBtn = document.querySelector("#update");
updateBtn.addEventListener("click", () => {
    document.getElementById("light_sc").style.display = "block";
    document.getElementById("faded_sc").style.display = "block";
})