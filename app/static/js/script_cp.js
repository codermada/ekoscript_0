function deleteConcept(concept_id, story_id) {
    let confirmed = window.confirm('Are you sure you want to delete this concept?');
    if (confirmed) {
        fetch(`/concept/delete-concept`, {
        method: "POST",
        body: JSON.stringify({concept_id: concept_id}) 
        }).then((_res)=> {
            window.location.href = `/concept/?id=${story_id}`;
        })
    }
    
}


const updateBtn = document.querySelector("#update");
updateBtn.addEventListener("click", () => {
    document.getElementById("light_cp").style.display = "block";
    document.getElementById("faded_cp").style.display = "block";
})

