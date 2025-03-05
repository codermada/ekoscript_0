function deleteGroup(group_id, story_id) {
    let confirmed = window.confirm('Are you sure you want to delete this group?');
    if (confirmed) {
        fetch(`/group/delete-group`, {
        method: "POST",
        body: JSON.stringify({group_id: group_id}) 
        }).then((_res)=> {
            window.location.href = `/group/?id=${story_id}`;
        })
    }
    
}

function include(group_id, supgroup_id) {
    let confirmed = window.confirm('Are you sure you want to include this group from that supgroup?');
    if (confirmed) {
        fetch(`/group/inclusion`, {
        method: "POST",
        body: JSON.stringify({group_id: group_id, supgroup_id: supgroup_id}) 
        }).then((_res)=> {
            window.location.href = `/group/group?id=${group_id}`;
        })
    }
    
}

function exclude(group_id, supgroup_id) {
    let confirmed = window.confirm('Are you sure you want to exclude this group from that supgroup?');
    if (confirmed) {
        fetch(`/group/exclusion`, {
        method: "POST",
        body: JSON.stringify({group_id: group_id, supgroup_id: supgroup_id}) 
        }).then((_res)=> {
            window.location.href = `/group/group?id=${group_id}`;
        })
    }
    
}
const updateBtn = document.querySelector("#update");
updateBtn.addEventListener("click", () => {
    document.getElementById("light_g").style.display = "block";
    document.getElementById("faded_g").style.display = "block";
})