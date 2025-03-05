function deleteAlbum(album_id, story_id) {
    let confirmed = window.confirm('Are you sure you want to delete this album?');
    if (confirmed) {
        fetch(`/album/delete-album`, {
        method: "POST",
        body: JSON.stringify({album_id: album_id}) 
        }).then((_res)=> {
            window.location.href = `/album/?id=${story_id}`;
        })
    }
    
}


const updateBtn = document.querySelector("#update");
updateBtn.addEventListener("click", () => {
    document.getElementById("light_album").style.display = "block";
    document.getElementById("faded_album").style.display = "block";
})