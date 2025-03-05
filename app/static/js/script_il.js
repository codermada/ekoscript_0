function delete_illustration(illustration_id, character_id){
    let confirmed = window.confirm('Are you sure you want to delete this illustration?');
    if (confirmed) {
        fetch(`/illustration/delete-illustration`, {
        method: "POST",
        body: JSON.stringify({illustration_id: illustration_id}) 
        }).then((_res)=> {
            window.location.href = `/illustration/?id=${character_id}`;
        })
    }
}

function update(illustration_id){
    let confirmed = window.confirm('Are you sure you want to update this description?');
    if (confirmed) {
        let desc = window.prompt('description');
        fetch(`/illustration/update`, {
        method: "POST",
        body: JSON.stringify({illustration_id: illustration_id, desc: desc}) 
        }).then((_res)=> {
            window.location.href = `/illustration/illustration?id=${illustration_id}`;
        })
    }
}