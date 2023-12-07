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
                     document.getElementById('processingDialog').style.display = 'none'
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

function diffSearch() {
  let diffInputValue = document.getElementById('diff-input').value
  if (diffInputValue === '') {
      document.getElementById('results').innerHTML = ''
      alert('empty input')
  } else {
      document.getElementById('processingDialog').style.display = 'block'
      postData({'search': diffInputValue}, 'diff', 'results')
  }
}

function tableSearch() {
  let tableInputValue = document.getElementById('table-input').value
  if (tableInputValue === '') {
      document.getElementById('results').innerHTML = ''
      alert('empty input')
  } else {
      document.getElementById('processingDialog').style.display = 'block'
      postData({'search': tableInputValue}, 'table', 'results')
  }
}

function startImport() {
  let importInputValue = document.getElementById('import-input').value
  if (importInputValue === '') {
      alert('empty input')
  } else {
      document.getElementById('processingDialog').style.display = 'block'
      postData({'path': importInputValue}, 'import', 'results')
  }
}

function startCompare() {
  let compareInputValue = document.getElementById('compare-input').value
  if (compareInputValue === '') {
      alert('empty input')
  } else {
      document.getElementById('processingDialog').style.display = 'block'
      postData({'path': compareInputValue}, 'compare', 'results')
  }
}


