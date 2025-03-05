function deleteSpot(spot_id, environement_id) {
    let confirmed = window.confirm('Are you sure you want to delete this spot?');
    if (confirmed) {
        fetch(`/spot/delete-spot`, {
        method: "POST",
        body: JSON.stringify({spot_id: spot_id}) 
        }).then((_res)=> {
            window.location.href = `/spot/?id=${environement_id}`;
        })
    }
    
}

const updateBtn = document.querySelector("#update");
updateBtn.addEventListener("click", () => {
    document.getElementById("light_spot").style.display = "block";
    document.getElementById("faded_spot").style.display = "block";
})