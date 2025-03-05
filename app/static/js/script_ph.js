function delete_photo(photo_id, album_id){
    let confirmed = window.confirm('Are you sure you want to delete this photo?');
    if (confirmed) {
        fetch(`/photo/delete-photo`, {
        method: "POST",
        body: JSON.stringify({photo_id: photo_id}) 
        }).then((_res)=> {
            window.location.href = `/photo/?id=${album_id}`;
        })
    }
}

function update(photo_id){
    let confirmed = window.confirm('Are you sure you want to update this description?');
    if (confirmed) {
        let desc = window.prompt('description');
        fetch(`/photo/update`, {
        method: "POST",
        body: JSON.stringify({photo_id: photo_id, desc: desc}) 
        }).then((_res)=> {
            window.location.href = `/photo/photo?id=${photo_id}`;
        })
    }
}