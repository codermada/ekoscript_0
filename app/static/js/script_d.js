function deleteChapter(division_id, panel_id) {
    let confirmed = window.confirm('Are you sure you want to delete this division?');
    if (confirmed) {
        fetch(`/division/delete-division`, {
        method: "POST",
        body: JSON.stringify({division_id: division_id}) 
        }).then((_res)=> {
            window.location.href = `/division/?id=${panel_id}`;
        })
    }
    
}
const updateBtn = document.querySelector("#update");
updateBtn.addEventListener("click", () => {
    document.getElementById("light_d").style.display = "block";
    document.getElementById("faded_d").style.display = "block";
})