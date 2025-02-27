// By Mohammad Alomar, 27 Feb 2025.
async function whitelist(route, method) {
    let response = await fetch('/get_whitelist')
    let whitelistPreAction = await response.text()
    let value = prompt(`whitelist = ${whitelistPreAction}`)
    if (!value) return
    let formData = new FormData()
    formData.append('value', value)
    response = await fetch(route, {method: method, body: formData})
    let whitelistPostAction = await response.text()
    alert(`whitelist = ${whitelistPostAction}`)
}

async function autoGroup() {
    let response = await fetch('/auto_group')
    response = await response.text()
    alert(response)
}

async function exportProject() {
    let response = await fetch('/export_project')
    let blob = await response.blob()
    let a = document.createElement('a')
    let url = URL.createObjectURL(blob)
    a.href = url
    a.download = 'acrm.zip'
    a.click()
    URL.revokeObjectURL(url)
}

async function importCrs() {
    let file = document.querySelector('input[type="file"]').files[0]
    let formData = new FormData()
    formData.append('file', file)
    let response = await fetch('/import_crs', {method: 'POST', body: formData})
    response = await response.text()
    alert(response)
}