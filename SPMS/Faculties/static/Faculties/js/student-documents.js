document.getElementById("filter-button").addEventListener('click', async function() {
    // Get search filters
    let queryParam = "?";

    // Username Filter
    const username_f = document.getElementById("username-filter").value
    if (!(username_f == "")) {
        queryParam = `${queryParam}username=${username_f}`
    }

    // Document Filter
    const type_f = document.getElementById("type-filter").value
    if (!(type_f == "0")){
        if (queryParam == "/?") {
            queryParam = `${queryParam}type=${type_f}`
        } else {
            queryParam = `${queryParam}&type=${type_f}`
        }
    }

    // Extension Filter
    const ext_f = document.getElementById("extension-filter").value
    if (!(ext_f =="0")){
        if (queryParam == "/?") {
            queryParam = `${queryParam}ext=${ext_f}`
        } else {
            queryParam = `${queryParam}&ext=${ext_f}`
        }
    }

    // Date filter
    const date_f = document.getElementById("date-filter").value
    if (!(date_f =="0")){
        if (queryParam == "/?") {
            queryParam = `${queryParam}date=${date_f}`
        } else {
            queryParam = `${queryParam}&date=${date_f}`
        }
    }

    // If empty
    if (queryParam == "?") {
        queryParam = "";
    }

    const container = document.getElementById('document-container')

    url = `http://localhost:8000/faculties/student_documents/filter/${queryParam}`;
    const rawData = await retrieveData(url)

    container.innerHTML = documentTableRowTemplate(rawData)
    
})

function documentTableRowTemplate(rawData) {
    let rows = '';
    rawData.forEach(data => {
        let id = data.id
        let name = data.SP.profile.full_name
        let type = data.SD_doc_type.document_type
        let file_url = data.SD_document
        let file_name = file_url.substring(7);
        let description = data.SD_doc_type.description
        let comments = data.SD_comment
        let last_modified = formatDate(data.SD_date_uploaded)

        if (comments == null) {
            comments = "None"
        }

        rows += `
            <tr>
                <td>${name}</td>
                <td>${type}</td>
                <td>${file_url ? `<a href="${file_url}" target="_blank">${file_name}</a>` : 'None'}</td>
                <td>${description}</td>
                <td>${comments}</td>
                <td>${last_modified}</td>
                <td class="text-center" style="font-size: 20px;">
                    <a href="#" class="text-primary mr-2"><i class='bx bx-edit'></i></a>
                    <a href="#" class="text-danger"><i class='bx bx-trash'></i></a>
                </td>
            </tr>
        `;
    });

    return rows;
}

documentSelectorBtn()

function documentSelectorBtn() {
    const editBtns = document.querySelectorAll("a[name='doc-edit-btn']")

    editBtns.forEach(btn => {
        var id = btn.id.split("-")[3]
        btn.addEventListener('click', function() {
            editDocument(id)
        })
    })
}

function editDocument(id) {
    // Get all values
    const type = document.getElementById(`doc-type-${id}`).getAttribute('data-value');
    const comment = document.getElementById(`doc-comment-${id}`).textContent
    const file = document.getElementById(`doc-file-${id}`).getAttribute("href");

    // Set the values to the form
    const typeSelect = document.getElementById("doc-edit-type")
    typeSelect.value = type

    const commentContainer = document.getElementById("doc-edit-comment")
    commentContainer.value = comment

    const fileContainer = document.getElementById("doc-edit-file")
    fileContainer.href = file
    fileContainer.textContent = file

    // const type_form = document.getElementById('doc-edit-type')
}


function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric', 
        hour: 'numeric', 
        minute: 'numeric' 
    };
    return date.toLocaleDateString('en-US', options).replace(',', '');
}

async function retrieveData (url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        return null;
    }

}


