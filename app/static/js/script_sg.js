function deleteSupgroup(supgroup_id, story_id) {
    let confirmed = window.confirm('Are you sure you want to delete this supgroup?');
    if (confirmed) {
        fetch(`/supgroup/delete-supgroup`, {
        method: "POST",
        body: JSON.stringify({supgroup_id: supgroup_id}) 
        }).then((_res)=> {
            window.location.href = `/supgroup/?id=${story_id}`;
        })
    }
    
}

const updateBtn = document.querySelector("#update");
updateBtn.addEventListener("click", () => {
    document.getElementById("light_sg").style.display = "block";
    document.getElementById("faded_sg").style.display = "block";
})