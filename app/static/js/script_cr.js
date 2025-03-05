function deleteCharacter(character_id, story_id) {
    let confirmed = window.confirm('Are you sure you want to delete this character?');
    if (confirmed) {
        fetch(`/character/delete-character`, {
        method: "POST",
        body: JSON.stringify({character_id: character_id}) 
        }).then((_res)=> {
            window.location.href = `/character/?id=${story_id}`;
        })
    }
    
}

function include(character_id, group_id) {
    let confirmed = window.confirm('Are you sure you want to include this character into that group?');
    if (confirmed) {
        fetch(`/character/inclusion`, {
        method: "POST",
        body: JSON.stringify({character_id: character_id, group_id: group_id}) 
        }).then((_res)=> {
            window.location.href = `/character/character?id=${character_id}`;
        })
    }
    
}

function exclude(character_id, group_id) {
    let confirmed = window.confirm('Are you sure you want to exclude this character from that group?');
    if (confirmed) {
        fetch(`/character/exclusion`, {
        method: "POST",
        body: JSON.stringify({character_id: character_id, group_id: group_id}) 
        }).then((_res)=> {
            window.location.href = `/character/character?id=${character_id}`;
        })
    }
    
}

function include2(character_id, supcharacter_id) {
    let confirmed = window.confirm('Are you sure you want to include this character into that supcharacter?');
    if (confirmed) {
        fetch(`/character/inclusion2`, {
        method: "POST",
        body: JSON.stringify({character_id: character_id, supcharacter_id: supcharacter_id}) 
        }).then((_res)=> {
            window.location.href = `/character/character?id=${character_id}`;
        })
    }
    
}

function exclude2(character_id, supcharacter_id) {
    let confirmed = window.confirm('Are you sure you want to exclude this character from that supcharacter?');
    if (confirmed) {
        fetch(`/character/exclusion2`, {
        method: "POST",
        body: JSON.stringify({character_id: character_id, supcharacter_id: supcharacter_id}) 
        }).then((_res)=> {
            window.location.href = `/character/character?id=${character_id}`;
        })
    }
    
}
const updateBtn = document.querySelector("#update");
updateBtn.addEventListener("click", () => {
    document.getElementById("light_character").style.display = "block";
    document.getElementById("faded_character").style.display = "block";
})