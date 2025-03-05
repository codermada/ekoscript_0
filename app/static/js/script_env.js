function deleteEnvironement(environement_id, story_id) {
    let confirmed = window.confirm('Are you sure you want to delete this environement?');
    if (confirmed) {
        fetch(`/environement/delete-environement`, {
        method: "POST",
        body: JSON.stringify({environement_id: environement_id}) 
        }).then((_res)=> {
            window.location.href = `/environement/?id=${story_id}`;
        })
    }
    
}


const updateBtn = document.querySelector("#update");
updateBtn.addEventListener("click", () => {
    document.getElementById("light_env").style.display = "block";
    document.getElementById("faded_env").style.display = "block";
})