// By Mohammad Alomar, 27 Feb 2025.
window.onload = home()

async function home() {

    let response = await fetch('/get_crs')
    let crs = await response.json()
    let table = document.createElement('table')
    let groupsNames = ['🚨 Follow Up', '🚫 Ignore', '🏁 Deployed']
    let tbodyElements = {}

    for (let groupName of groupsNames)
        tbodyElements[groupName] = document.createElement('tbody')

    for (let cr of crs) {

        let [crid, title, state, assignee, email, group, comment] = cr

        // crid
        let cridElement = document.createElement('a')
        cridElement.textContent = crid
        cridElement.href = ``
        cridElement.target = '_blank'

        // title
        let titleElement = document.createElement('p')
        titleElement.textContent = titleElement.title = title

        // state
        let stateElement = document.createElement('p')
        stateElement.textContent = state

        // assignee
        let assigneeElement = document.createElement('a')
        assigneeElement.title = assignee
        if (assignee.split(' ').length > 2) assignee = assignee.split(' ')[0] + ' ' + assignee.split(' ').pop()
        assigneeElement.textContent = assignee
        let cc = ''
        let subject =`${crid} - ${title}`
        let body = `Dear ${assignee},` 
            + `%0A` + `I hope you're doing well.` 
            + `%0A` + `I wanted to check in on the status of the change request.` 
            + `%0A` + `Could you provide an update on where things stand and let me know if any support is needed?` 
            + `%0A` + `Looking forward to your response. Thanks!`
            + `%0A` + ` `
            + `%0A` + `${crid}`
            + `%0A` + `${title}`
            + `%0A` + `${cridElement.href}`
        assigneeElement.href = `mailto:${email};?cc=${cc}&subject=${subject}&body=${body}`

        // group
        let groupElement = document.createElement('select')
        groupElement.onchange = () => patchGroup(crid, groupElement)
        for (let groupName of groupsNames) {
            let option = document.createElement('option')
            option.value = option.textContent = groupName
            if (group == groupName) option.selected = true
            groupElement.appendChild(option)
        }

        // comment
        let commentElement = document.createElement('p')
        commentElement.textContent = commentElement.title = comment
        commentElement.onclick = () => patchComment(crid, commentElement)

        // table row
        let tr = document.createElement('tr')
        for (let element of [cridElement, titleElement, stateElement, assigneeElement, groupElement, commentElement]) {
            let td = document.createElement('td')
            td.appendChild(element)
            tr.appendChild(td)
        }

        tbodyElements[group].appendChild(tr)

    }

    for (let groupName in tbodyElements)
        table.appendChild(tbodyElements[groupName])

    document.body.replaceChildren(table)

}

async function patchGroup(crid, groupElement) {
    let formData = new FormData()
    formData.append('crid', crid)
    formData.append('value', groupElement.value)
    await fetch('/patch_group', {method: 'PATCH', body: formData})
    home()
}

async function patchComment(crid, commentElement) {
    let comment = prompt(commentElement.title)
    if (!comment) return
    let formData = new FormData()
    formData.append('crid', crid)
    formData.append('value', comment)
    await fetch('/patch_comment', {method: 'PATCH', body: formData})
    home()
}