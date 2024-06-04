// Set Tabs
document.getElementById("Tab1").style.display = "block";
document.getElementById("tab-btn-1").classList.add("active-button")
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active-button", "");
    }

    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active-button";
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


function personalInformationTemplate(data) {
    var profileData = data.profile
    document.getElementById("pi-img").src = profileData.image
    document.getElementById("pi-id").value = data.id
    setupDisplayAndEdit(document.getElementById("pi-un"), profileData.username);
    setupDisplayAndEdit(document.getElementById("pi-fln"), profileData.full_name);
    setupDisplayAndEdit(document.getElementById("pi-fn"), profileData.first_name);
    setupDisplayAndEdit(document.getElementById("pi-ln"), profileData.last_name);
    setupDisplayAndEdit(document.getElementById("pi-email"), profileData.email);
    setupDisplayAndEdit(document.getElementById("pi-univ-email"), profileData.university_email);
    setupDisplayAndEdit(document.getElementById("pi-dob"), profileData.DOB);
    setupDisplayAndEdit(document.getElementById("pi-contact"), profileData.contact);
    setupDisplayAndEdit(document.getElementById("pi-sex"), profileData.sex);
}


function setupDisplayAndEdit(node, data) {
    node.querySelector("p").textContent = data;

    // Check if its input or a select
    if (node.querySelector("input")) {
        node.querySelector("input").value = data;
        node.querySelector("input").classList.add("hidden");
    } else if (node.querySelector("select")){
        node.querySelector("select").value = data;
        node.querySelector("select").classList.add("hidden");
    }

}


// Set the interface in edit
function profileInfoEditMode() {
    const id_tab = document.getElementById("pi");
    const inputs = id_tab.querySelectorAll("td")

    document.getElementById("pi-edit-mode").classList.remove("hidden")
    document.getElementById("pi-read-mode").classList.add("hidden")

    inputs.forEach(input=>{
        input.lastElementChild.classList.remove("hidden")
        input.firstElementChild.classList.add("hidden")
    })
}


// Set the interface in read mode
function profileInfoReadMode() {
    const id_tab = document.getElementById("pi");
    const inputs = id_tab.querySelectorAll("td")

    document.getElementById("pi-edit-mode").classList.add("hidden")
    document.getElementById("pi-read-mode").classList.remove("hidden")

    inputs.forEach(input=>{
        input.lastElementChild.classList.add("hidden")
        input.firstElementChild.classList.remove("hidden")
    })
}


function openStudentDetails(id) {
    const listDiv = document.getElementById("student-list")
    const detailDiv = document.getElementById("student-detail")

    listDiv.style.display = "none";
    detailDiv.style.display = "block";
}


function openStudentList() {
    const listDiv = document.getElementById("student-list")
    const detailDiv = document.getElementById("student-detail")
    profileInfoReadMode()

    listDiv.style.display = "block";
    detailDiv.style.display = "none";
}


function profileInfoSave() {
    const id = document.getElementById("pi-id").value;
    const un = document.getElementById("pi-un").lastElementChild.value
    const fn = document.getElementById("pi-fn").lastElementChild.value
    const ln = document.getElementById("pi-ln").lastElementChild.value
    const email = document.getElementById("pi-email").lastElementChild.value
    const univ_email = document.getElementById("pi-univ-email").lastElementChild.value
    const dob = document.getElementById("pi-dob").lastElementChild.value
    const contact = document.getElementById("pi-contact").lastElementChild.value
    const sex = document.getElementById("pi-sex").lastElementChild.value

    const url = "http://localhost:8000/faculties/student_profiles/update/"
    const data = {
        id:id,
        username: un,
        first_name: fn,
        last_name: ln,
        email: email,
        univ_email: univ_email,
        dob: dob,
        contact: contact,
        sex: sex
    };


    const options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: JSON.stringify(data)
    };


    fetch(url, options)
        .then(response => {
            if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
                alert("Cannot process events now! Try again later.");
            }
            
            return response.json(); // Parse the JSON response
        })
        .then(data => {

            if ('error' in data){
                alert(data.error)
                console.log("error")
            } else {
                console.log("1")
                alert("Update successful");
                profileInfoReadMode()
                retrievePersonalInformation(id)
            }
            return;

        })
        .catch(error => {
            console.log(error)
            alert("Cannot process! Try again later.")
        });
}

// ********************************************** FAMILY RECORDS RELATED ***************************************************
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

async function load_familyRecords() {
    const id = document.getElementById("pi-id").value
    url = `http://localhost:8000/faculties/student_profiles/family/?id=${id}`
    const rawData = await retrieveData(url)
    
    document.getElementById('fam-container').innerHTML = ""
    const data = rawData.results
    data.forEach(d =>{
        createFamilyMemberCard(d)
    })
}

function createFamilyMemberCard (data){
    const id = data.id
    const relationship = data.relationship
    const first_name = data.first_name
    const last_name = data.last_name
    const name = `${first_name} ${last_name}`
    const contact = data.contact
    const emergency = data.emergency_contact
    const relationshipOptions = ['Father', 'Mother', 'Sibling', 'Spouse', 'Guardian'];
    const placeholder_width = "100px";

    
    // Create main card container
    const card = document.createElement('div');
    card.classList.add('fam-profile-card', 'card', 'mb-3');
    card.setAttribute('id', `profile-card-${id}`);

    // Create card header
    const header = document.createElement('div');
    header.classList.add('fam-profile-header', 'card-header');
    const headerTitle = document.createElement('h3');
    headerTitle.textContent = name;
    header.appendChild(headerTitle);

    // Create card details
    const details = document.createElement('div');
    details.classList.add('fam-profile-details', 'card-body');
    const detailsContent = `
        <div class="row mb-2">
            <div class="col-6">
                <strong>Relationship:</strong>
                <span name="fam-d-${id}">${relationship}</span>
                <span class="hidden" name="fam-e-${id}">
                    <select id="relationship-${id}" class="form-select"">
                        ${relationshipOptions.map(option => `
                            <option value="${option}" ${relationship === option ? 'selected' : ''}>${option}</option>
                        `).join('')}
                    </select>
                </span>
            </div>
            <div class="col-6">
                <strong>Contact Number:</strong>
                <span name="fam-d-${id}">${contact}</span>
                <span class="hidden" name="fam-e-${id}"><input id="contact-${id}" class="form-control" type="text" value="${contact}"></span>
            </div>
        </div>
        <div class="row mb-2">
            <div class="col-6">
                <strong>First Name:</strong>
                <span name="fam-d-${id}">${first_name}</span>
                <span class="hidden" name="fam-e-${id}"><input id="first-name-${id}" class="form-control" type="text" value="${first_name}"></span>
            </div>
            <div class="col-6">
                <strong>Last name:</strong>
                <span name="fam-d-${id}">${last_name}</span>
                <span class="hidden" name="fam-e-${id}"><input id="last-name-${id}" class="form-control" type="text" value="${last_name}"></span>
            </div>
        </div>
        <div class="row mb-2">
            <div class="col-6">
                <strong>Emergency Contact:</strong>
                <span style="color:red; font-weight:bold;"name="fam-d-${id}">${emergency ? 'Yes' : 'No'}</span>
                <span class="hidden" name="fam-e-${id}">
                    <select class="form-select" id="emergency-${id}">
                        <option value="true" ${emergency ? 'selected' : ''}>Yes</option>
                        <option value="false" ${!emergency ? 'selected' : ''}>No</option>
                    </select>
                </span>
            </div>
        </div>
    `;
    details.innerHTML = detailsContent;

    const actions = document.createElement('div');
    actions.classList.add('fam-profile-actions', 'card-footer');
    const editButtons = document.createElement('div');
    editButtons.id=`edit-btns-${id}`
    editButtons.innerHTML = `
        <button class="btn btn-primary btn-sm mr-2 edit-btn">Edit</button>
        <button class="btn btn-danger btn-sm delete-btn">Delete</button>
    `;

    const saveButtons = document.createElement('div');
    saveButtons.classList.add('hidden')
    saveButtons.id=`save-btns-${id}`
    saveButtons.innerHTML = `
        <button class="btn btn-success btn-sm mr-2 save-btn">Save</button>
        <button class="btn btn-secondary btn-sm cancel-btn">Cancel</button>
    `;
    actions.appendChild(editButtons);
    actions.appendChild(saveButtons);

    // Add event listeners to buttons
    const editBtn = actions.querySelector('.edit-btn');
    const deleteBtn = actions.querySelector('.delete-btn');
    const saveBtn = actions.querySelector('.save-btn');
    const cancelBtn = actions.querySelector('.cancel-btn');

    editBtn.addEventListener('click', ()=> familyRecordMode(id,'w'))
    cancelBtn.addEventListener('click', ()=> familyRecordMode(id,'r'))
    saveBtn.addEventListener('click', ()=> saveFamilyRecord(id));
    deleteBtn.addEventListener('click', ()=> deleteFamRecordConfirm(id));
    deleteBtn.setAttribute("data-bs-toggle", "modal");
    deleteBtn.setAttribute("data-bs-target", "#deleteFamilyRecordModal");

    // Append header, details, and actions to the main card
    card.appendChild(header);
    card.appendChild(details);
    card.appendChild(actions);
    
    // Append card to the profile container
    document.getElementById('fam-container').appendChild(card);
}

function familyRecordMode(id,mode) {
    // mode can b r or w (read or write) write = edit

    // Change the buttons
    const editButtons = document.getElementById(`edit-btns-${id}`)
    const saveButtons = document.getElementById(`save-btns-${id}`)

    if (mode == 'w') {
        saveButtons.classList.remove('hidden')
        editButtons.classList.add('hidden')
    } else {
        saveButtons.classList.add('hidden')
        editButtons.classList.remove('hidden')
    }

    // Hide the displays
    const displays = document.querySelectorAll(`span[name='fam-d-${id}']`)
    displays.forEach(display=>{
        if (mode == "w") {
            display.classList.add('hidden');
        } else {
            display.classList.remove('hidden');
        }
    })

    // Show the forms
    const forms = document.querySelectorAll(`span[name='fam-e-${id}']`)
    forms.forEach(form=>{
        if (mode == "w") {
            form.style.display="inline-block";
            form.classList.remove('hidden');
        } else {
            form.style.display="none";
            form.classList.add('hidden');
        }
    })

}

async function saveFamilyRecord(id){
    const relationship = document.getElementById(`relationship-${id}`).value;
    const contact = document.getElementById(`contact-${id}`).value;
    const first_name = document.getElementById(`first-name-${id}`).value;
    const last_name = document.getElementById(`last-name-${id}`).value;
    const emergency = document.getElementById(`emergency-${id}`).value;

    const url = 'http://localhost:8000/faculties/student_profiles/family/update/';
    const data = {
        id:id,
        relationship:relationship,
        contact:contact,
        first_name:first_name,
        last_name:last_name,
        emergency:emergency
    }

    try {
        const responseData = await postData(url, data);
        if (responseData.success = "OK") {
            alert("Update successful");
            load_familyRecords()
        } else {
            alert("There was a problem processing this request! Try again later.")
        }
      } catch (error) {
        alert("There was a problem processing this request! Try again later.")
      }

}

function deleteFamRecordConfirm(id) {
    const btn = document.getElementById("del-fam-record-confirm")
    btn.onclick = async function () {
        deleteFamRecordConfirmed(id)
    }
}

async function deleteFamRecordConfirmed(id) {
    const btn = document.getElementById("del-fam-record-confirm")
    const modal = document.getElementById("deleteFamilyRecordModal")
    const modalCls = modal.querySelector(".btn-close");

    btn.disabled = true
    btn.textContent = "Deleting..."

    const url = 'http://localhost:8000/faculties/student_profiles/family/delete/';
    const data = {
        id:id,
    }

    try {
        const responseData = await postData(url, data);
        if (responseData.success = "OK") {
            alert("Delete Successful");
            load_familyRecords()
            modalCls.click()
            
        } else {
            alert("There was a problem processing this request! Try again later.")
        }
      } catch (error) {
        alert("There was a problem processing this request! Try again later.")
      }
    btn.disabled = false
    btn.textContent = "Delete"

}

document.getElementById("new-family-btn").addEventListener('click', async function(e){
    this.disabled = true
    this.textContent = "Adding..."

    const id = document.getElementById("pi-id").value
    const relationship = document.getElementById("new-relationship").value
    const contact = document.getElementById("new-contactNumber").value
    const first_name = document.getElementById("new-firstName").value
    const last_name = document.getElementById("new-lastName").value
    const emergency = document.getElementById("new-emergency").checked

    const modal = document.getElementById("addFamilyRecordModal")
    const modalCls = modal.querySelector(".btn-close");

    const url = 'http://localhost:8000/faculties/student_profiles/family/add/';
    const data = {
        id:id,
        relationship:relationship,
        contact:contact,
        first_name:first_name,
        last_name:last_name,
        emergency:emergency
    }

    try {
        const responseData = await postData(url, data);
        if (responseData.success = "OK") {
            alert("Update successful");
            load_familyRecords()
            modalCls.click()
        } else {
            alert("There was a problem processing this request! Try again later.")
        }
      } catch (error) {
        alert("There was a problem processing this request! Try again later.")
      }
    this.disabled = false
    this.textContent = "Add"

})

// ************************************************ EDUCATION RECORDS RELATED ********************************************
async function retrievePersonalInformation (id){
    const url = `http://localhost:8000/faculties/student_profiles/detail/?id=${id}`;
    const data = await retrieveData(url);

    personalInformationTemplate(data)
    load_familyRecords()
    load_educRecords()
}

async function load_educRecords(){
    const id = document.getElementById("pi-id").value
    url = `http://localhost:8000/faculties/student_profiles/education/?id=${id}`
    const rawData = await retrieveData(url)

    document.getElementById('educ-container').innerHTML = ""
    const data = rawData.results

    data.forEach(d=>{
        createEducationCard(d)
    })
}


function createEducationCard(data) {
    const id = data.id
    const level = data.level
    const institution = data.institution
    const address = data.address
    const description = data.description
    const year = data.year
    const LEVEL_LIST = ['Primary', 'Secondary', 'Tertiary', 'Vocational', 'Post-Graduate']

    // Create main card container
    const card = document.createElement('div');
    card.classList.add('education-card');
    card.setAttribute('id', `education-card-${id}`);
    
    // Create Card header
    const header = document.createElement('div');
    header.classList.add('education-header');
    const headerTitle = document.createElement('h5');
    headerTitle.textContent = level;
    const headerDate = document.createElement("span")
    headerDate.textContent = year
    header.appendChild(headerTitle);
    header.appendChild(headerDate)

    const details = document.createElement('div');
    const detailsContent = `
    <div>
        <p><strong>Level:</strong> 
            <span name="educ-d-${id}">${level}</span>
            <span name="educ-e-${id}" class="hidden">
                <select id="level-${id}" class="form-select"">
                ${LEVEL_LIST.map(option => `
                    <option value="${option}" ${level === option ? 'selected' : ''}>${option}</option>
                `).join('')}
            </select>
            </span>
        </p>
        <p><strong>Institution:</strong> 
            <span name="educ-d-${id}">${institution}</span>
            <span name="educ-e-${id}" class="hidden">
                <input id="institution-${id}" class="form-control" type="text" value="${institution}">
            </span>
        </p>
        <p><strong>Address:</strong> 
            <span name="educ-d-${id}">${address}</span>
            <span name="educ-e-${id}" class="hidden">
                <input id="address-${id}" class="form-control" type="text" value="${address}">
            </span>
        </p>
        <p><strong>Description:</strong> 
            <span name="educ-d-${id}">${description}</span>
            <span name="educ-e-${id}" class="hidden">
                <textarea id="description-${id}" class="form-control" cols="80" placeholder="Enter Description">${description}</textarea>
            </span>
        </p>
        <p class="hidden" id="hidden-year-${id}"><strong>Year:</strong> 
            <span name="educ-e-${id}" class="hidden">
                <input id="year-${id}" class="form-control" type="number" value="${year}">
            </span>
        </p>
    </div>
    `

    details.innerHTML = detailsContent

    const actions = document.createElement('div');
    actions.classList.add('education-card-actions');

    const editButtons = document.createElement('div');
    editButtons.id=`educ-edit-btns-${id}`
    editButtons.innerHTML = `
        <button class="btn btn-primary btn-sm mr-2 edit-btn">Edit</button>
        <button class="btn btn-danger btn-sm delete-btn">Delete</button>
    `;

    const saveButtons = document.createElement('div');
    saveButtons.classList.add('hidden')
    saveButtons.id=`educ-save-btns-${id}`
    saveButtons.innerHTML = `
        <button class="btn btn-success btn-sm mr-2 save-btn">Save</button>
        <button class="btn btn-secondary btn-sm cancel-btn">Cancel</button>
    `;

    // Add event listeners to buttons
    const editBtn = editButtons.querySelector('.edit-btn');
    const deleteBtn = editButtons.querySelector('.delete-btn');
    const saveBtn = saveButtons.querySelector('.save-btn');
    const cancelBtn = saveButtons.querySelector('.cancel-btn');

    editBtn.addEventListener('click', ()=> educRecordMode(id,'w'))
    cancelBtn.addEventListener('click', ()=> educRecordMode(id,'r'))
    saveBtn.addEventListener('click', ()=> saveEducRecord(id))
    deleteBtn.addEventListener('click', ()=> deleteEducRecordConfirm(id));
    deleteBtn.setAttribute("data-bs-toggle", "modal");
    deleteBtn.setAttribute("data-bs-target", "#deleteEducationBGModal");

    actions.appendChild(editButtons);
    actions.appendChild(saveButtons);

    card.appendChild(header)
    card.appendChild(details)
    card.appendChild(actions)

    document.getElementById('educ-container').appendChild(card)

}


function educRecordMode(id, mode){
    // mode can b r or w (read or write) write = edit

    // Change the buttons
    const editButtons = document.getElementById(`educ-edit-btns-${id}`)
    const saveButtons = document.getElementById(`educ-save-btns-${id}`)
    const hiddenYear = document.getElementById(`hidden-year-${id}`)

    if (mode == 'w') {
        saveButtons.classList.remove('hidden')
        editButtons.classList.add('hidden')
        hiddenYear.classList.remove('hidden')
    } else {
        hiddenYear.classList.add('hidden')
        saveButtons.classList.add('hidden')
        editButtons.classList.remove('hidden')
    }

    // Hide the displays
    const displays = document.querySelectorAll(`span[name='educ-d-${id}']`)
    displays.forEach(display=>{
        if (mode == "w") {
            display.classList.add('hidden');
        } else {
            display.classList.remove('hidden');
        }
    })

    // Show the forms
    const forms = document.querySelectorAll(`span[name='educ-e-${id}']`)
    forms.forEach(form=>{
        if (mode == "w") {
            form.style.display="inline-block";
            form.classList.remove('hidden');
        } else {
            form.style.display="none";
            form.classList.add('hidden');
        }
    })
}


async function saveEducRecord(id) {
    const level = document.getElementById(`level-${id}`).value
    const institution = document.getElementById(`institution-${id}`).value
    const address = document.getElementById(`address-${id}`).value
    const description = document.getElementById(`description-${id}`).value
    const year = document.getElementById(`year-${id}`).value

    const url = 'http://localhost:8000/faculties/student_profiles/education/update/';
    const data = {
        id:id,
        level:level,
        institution:institution,
        address:address,
        description:description,
        year:year
    }

    try {
        const responseData = await postData(url, data);
        if (responseData.success = "OK") {
            alert("Update successful");
            load_educRecords()
        } else {
            alert("There was a problem processing this request! Try again later.")
        }
      } catch (error) {
        alert("There was a problem processing this request! Try again later.")
      }

}


function deleteEducRecordConfirm(id) {
    const btn = document.getElementById("del-educ-record-confirm")
    btn.onclick = async function () {
        deleteEducRecordConfirmed(id)
    }
}

async function deleteEducRecordConfirmed(id) {
    const btn = document.getElementById("del-educ-record-confirm")
    const modal = document.getElementById("deleteEducationBGModal")
    const modalCls = modal.querySelector(".btn-close");

    btn.disabled = true
    btn.textContent = "Deleting..."

    const url = 'http://localhost:8000/faculties/student_profiles/education/delete/';
    const data = {
        id:id,
    }

    try {
        const responseData = await postData(url, data);
        if (responseData.success = "OK") {
            alert("Delete Successful");
            load_educRecords()
            modalCls.click()
        } else {
            alert("There was a problem processing this request! Try again later.")
        }
      } catch (error) {
        alert("There was a problem processing this request! Try again later.")
      }
    btn.disabled = false
    btn.textContent = "Delete"
}

document.getElementById("new-educ-form").addEventListener('submit', async function(e){
    e.preventDefault()
    const btn = this.querySelector("#new-educ-btn")
    btn.disabled = true
    btn.textContent = "Adding..."

    const id = document.getElementById("pi-id").value
    const level = document.getElementById("new-level").value
    const institution = document.getElementById("new-institution").value
    const address = document.getElementById("new-address").value
    const description = document.getElementById("new-description").value
    const year = document.getElementById("new-year").value

    const modal = document.getElementById("addEducBgRecordModal")
    const modalCls = modal.querySelector(".btn-close");

    const url = 'http://localhost:8000/faculties/student_profiles/education/add/';
    const data = {
        id:id,
        level:level,
        institution:institution,
        address:address,
        description:description,
        year:year
    }

    try {
        const responseData = await postData(url, data);
        if (responseData.success = "OK") {
            alert("Update successful");
            load_educRecords()
            modalCls.click()
        } else {
            alert("There was a problem processing this request! Try again later.")
        }
      } catch (error) {
        alert("There was a problem processing this request! Try again later.")
      }
    btn.disabled = false
    btn.textContent = "Add"

})
