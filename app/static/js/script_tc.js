function erase(line_id, chapter_id) {
    let confirmed = window.confirm('confirm');
    if (confirmed){
        fetch('/chapter/erase',{
            method: 'POST',
            body: JSON.stringify({'line_id': line_id})
        }).then((res_)=>{
            window.location.href = `/chapter/full-text?id=${chapter_id}`
        })
    }
}

function update(line_id, chapter_id) {
    
    let confirmed = window.confirm('confirm');
    if (confirmed){
        let text = window.prompt('text');
        fetch('/chapter/update',{
        method: 'POST',
        body: JSON.stringify({'line_id': line_id, 'text': text})
        }).then((res_)=>{
            window.location.href = `/chapter/full-text?id=${chapter_id}`
        })
    }
    
}