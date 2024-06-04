// Filter Documents
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
    documentSelectorBtn()
    
})

// Add new Document Type
document.getElementById("addNewTypeForm").addEventListener('submit', async function(e) {
    e.preventDefault()

    const type = document.getElementById("addNewType").value
    const description = document.getElementById("addNewDescription").value
    const modal = document.getElementById("addNewTypeModal")
    const modalCls = modal.querySelector(".btn-close");

    const url = "http://localhost:8000/faculties/student_documents/type/add/"
    const data = {
        type: type,
        description: description
    }

    try {
        const responseData = await postData(url, data);
        if ('error' in responseData){
            alert(responseData.error)
        } else if (responseData.success = "OK") {
            alert("New Document Added");
            populateTypeFilter(responseData.updated)
            modalCls.click()
        } else {
            alert("Cannot process your request!")
        }
    } catch (error) {
        console.log("Error", error)
        alert("There was a problem processing this request! Try again later.")
    }

})


// Save Document
document.getElementById("doc-edit-form").addEventListener('submit', async function(e) {
    e.preventDefault()

    console.log("Hello")

    const type = document.getElementById("doc-edit-type").value
    const comment = document.getElementById("doc-edit-comment").value
    const id = document.getElementById("doc-edit-id").value
    const file = document.getElementById("doc-edit-file").files[0]
    const clear = document.getElementById("edit-doc-clear").checked

    const modal = document.getElementById("doc-edit-formModal")
    const modalCls = modal.querySelector(".btn-close");

    const formData = new FormData();
    formData.append("id", id)
    formData.append("type", type)
    formData.append("comment", comment)
    formData.append("file", file)
    formData.append("clear", clear)
    
    const url = "http://localhost:8000/faculties/student_documents/update/"

    try {
        const responseData = await postData1(url, formData);
        console.log(responseData)
        if (responseData.success = "OK") {
            alert("Document updated");
            updateDocumentRow(id, responseData.updated)
            modalCls.click()
        } else {
            alert("Cannot process your request!")
        }
    } catch (error) {
        alert("There was a problem processing this request! Try again later.")
    }
})


function documentTableRowTemplate(rawData) {
    let rows = '';
    rawData.forEach(data => {
        let id = data.id
        let name = data.SP.profile.full_name
        let type = data.SD_doc_type.document_type
        let file_url = data.SD_document
        let description = data.SD_doc_type.description
        let comments = data.SD_comment
        let last_modified = formatDate(data.SD_date_uploaded)

        if (comments == null) {
            comments = "None"
        }

        rows += `
            <tr>
                <td id="doc-description-${id}">${name}</td>
                <td id="doc-type-${id}" data-value="${data.SD_doc_type.id}">${type}</td>
                <td>${file_url ? `<a id="doc-file-${id}" href="${file_url}" target="_blank">${file_url.substring(7)}</a>` : 'None'}</td>
                <td id="doc-description-${id}">${description}</td>
                <td id="doc-comment-${id}">${comments}</td>
                <td id="doc-date-${id}">${last_modified}</td>
                <td class="text-center" style="font-size: 20px;">
                    <a href="#" name="doc-edit-btn" data-bs-toggle="modal" data-bs-target="#doc-edit-formModal" id="doc-edit-btn-${id}" class="text-primary mr-2"><i class='bx bx-edit'></i></a>
                    <a href="#" class="text-danger"><i class='bx bx-trash'></i></a>
                </td>
            </tr>
        `;
    });

    return rows;
}


documentSelectorBtn() // For initial values
// Set up the edit button for the documents
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
    console.log(document.getElementById("edit-doc-clear").checked)
    document.getElementById("edit-doc-clear").checked = false
    console.log(document.getElementById("edit-doc-clear").checked)

    // Set the values to the form
    const idContainer = document.getElementById("doc-edit-id")
    idContainer.value = id

    const typeSelect = document.getElementById("doc-edit-type")
    typeSelect.value = type

    const commentContainer = document.getElementById("doc-edit-comment")
    commentContainer.value = comment

    const fileContainer = document.getElementById("current-file")
    fileContainer.href = file
    fileContainer.textContent = file

}

function populateTypeFilter(data) {
    const select = document.getElementById("type-filter")
    select.innerHTML = ""
    var option = document.createElement("option")
    option.value = 0
    option.textContent = "Type"
    select.append(option)

    data.forEach(d=>{
        option = document.createElement("option")
        option.value = d.id
        option.textContent = d.document_type
        select.appendChild(option)
    })
}

function updateDocumentRow(id,data) {
    let name = data.SP.profile.full_name
    let type = data.SD_doc_type.document_type
    let file_url = data.SD_document
    let description = data.SD_doc_type.description
    let comments = data.SD_comment
    let last_modified = formatDate(data.SD_date_uploaded)

    const newname = document.getElementById(`doc-name-${id}`)
    const newtype = document.getElementById(`doc-type-${id}`)
    const newfile = document.getElementById(`doc-file-${id}`)
    const newdescription = document.getElementById(`doc-description-${id}`)
    const newcomment = document.getElementById(`doc-comment-${id}`)
    const newdate = document.getElementById(`doc-date-${id}`)

    newname.textContent = name
    newtype.textContent = type
    newtype.setAttribute("data-value", data.SD_doc_type.id)
    newfile.textContent = file_url
    newfile.href = file_url
    newdescription.textContent = description
    newcomment.textContent = comments
    newdate.textContent = last_modified

    if (file_url != null) {
        newfile.textContent = file_url.substring(7);
        newfile.href = file_url.substring(7);
    }
}

async function postData1(url, data) {
    try {
      const response = await fetch(url, {
        method: 'POST',
        body: data,
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      const responseData = await response.json();
      return responseData;
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
}

async function postData(url, data) {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add any other headers here
        },
        body: JSON.stringify(data),
      });
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      const responseData = await response.json();
      return responseData;
    } catch (error) {
      console.error('Error:', error);
      throw error;
    }
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


