async function postData(postData, route, returnToId) {
    try {
        return await fetch(route, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(postData),
        }).then((response) => response.json())
                .then((data) => {return data})
    } catch (error) {
        alert('API error')
    }
}


function tableSearch() {
  let tableInput = document.getElementById('table-input').value
  if (tableInput === '') {
    alert('empty input')
  }
}