function exportTableToCSV() {
    const fileName = prompt('Enter a file name (without extension):');
    if (fileName === null || fileName.trim() === '') {
       return;
    }
    const fullFileName = fileName.trim() + '.csv';
    const table = document.getElementById('response-table');
    const rows = table.querySelectorAll('tr');
    const tableHead = table.querySelectorAll('th');
    const csv = [];

    let headData = []
    for (const row of tableHead) {
        console.log(row)
        headData.push(row.textContent);
    }
    csv.push(headData.join(','))

    for (const row of rows) {
        const cells = row.querySelectorAll('td');
        const rowData = [];
        for (const cell of cells) {
            rowData.push(cell.textContent);
        }
        if (rowData.length > 0) {
            csv.push(rowData.join(','));
        }
    }
    const csvData = csv.join('\n');
    const blob = new Blob([csvData], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fullFileName
    a.style.display = 'none';

    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}