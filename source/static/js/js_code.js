async function postData(postData, route, returnToId) {
    try {
        return await fetch(route, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(postData),
        }).then((response) => response.json())
                .then((resp) => {
                    console.log(resp)
                    let results = document.getElementById(returnToId)
                    if (resp['error']) {
                        results.innerHTML = ''
                        alert(resp['errorMsg'])
                    } else {
                        results.innerHTML = ''
                        results.innerHTML = resp['data']
                    }
                })
    } catch (error) {
        alert('API error')
    }
}


function tableSearch() {
  let tableInputValue = document.getElementById('table-input').value
  if (tableInputValue === '') {
      document.getElementById('results').innerHTML = ''
      alert('empty input')
  } else {
      postData({'search': tableInputValue}, 'table', 'results')
  }
}