async function retrievePersonalInformation (id){
    const url = `http://localhost:8000/faculties/student_profiles/detail/?id=${id}`;
    const data = await retrieveData(url);
    
    personalInformationTemplate(data)
}

function personalInformationTemplate(data) {
    var profileData = data.profile
    console.log()
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

