function deleteItem(item_id, story_id) {
    let confirmed = window.confirm('Are you sure you want to delete this item?');
    if (confirmed) {
        fetch(`/item/delete-item`, {
        method: "POST",
        body: JSON.stringify({item_id: item_id}) 
        }).then((_res)=> {
            window.location.href = `/item/?id=${story_id}`;
        })
    }
    
}


function include(item_id, supitem_id) {
    let confirmed = window.confirm('Are you sure you want to include this item from that supitem?');
    if (confirmed) {
        fetch(`/item/inclusion`, {
        method: "POST",
        body: JSON.stringify({item_id: item_id, supitem_id: supitem_id}) 
        }).then((_res)=> {
            window.location.href = `/item/item?id=${item_id}`;
        })
    }
    
}

function exclude(item_id, supitem_id) {
    let confirmed = window.confirm('Are you sure you want to exclude this item from that supitem?');
    if (confirmed) {
        fetch(`/item/exclusion`, {
        method: "POST",
        body: JSON.stringify({item_id: item_id, supitem_id: supitem_id}) 
        }).then((_res)=> {
            window.location.href = `/item/item?id=${item_id}`;
        })
    }
    
}
const updateBtn = document.querySelector("#update");
updateBtn.addEventListener("click", () => {
    document.getElementById("light_i").style.display = "block";
    document.getElementById("faded_i").style.display = "block";
})

