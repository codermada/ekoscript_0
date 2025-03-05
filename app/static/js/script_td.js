function erase(text_id, division_id) {
    let confirmed = window.confirm('confirm');
    if (confirmed){
        fetch('/division/erase',{
            method: 'POST',
            body: JSON.stringify({'text_id': text_id})
        }).then((res_)=>{
            window.location.href = `/division/full-text?id=${division_id}`
        })
    }
}

function update(text_id, division_id) {
    
    let confirmed = window.confirm('confirm');
    if (confirmed){
        let text = window.prompt('text');
        fetch('/division/update',{
        method: 'POST',
        body: JSON.stringify({'text_id': text_id, 'text': text})
        }).then((res_)=>{
            window.location.href = `/division/full-text?id=${division_id}`
        }) 
    }
    
}