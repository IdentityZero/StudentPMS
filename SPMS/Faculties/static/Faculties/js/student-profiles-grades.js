async function retrieveStudentGrades(id){
    const url = `http://localhost:8000/faculties/student_profiles/grades/?id=${id}`
    const gradeTable = document.getElementById("grade-id")
    gradeTable.innerHTML = ""

    const data = await fetchData(url)

    for (var year in data) {
        if (data.hasOwnProperty(year)) {
            var sems = data[year]

            for (var sem in sems){
                var t = gradeTableTemplate(year,sem, sems[sem])
                gradeTable.appendChild(t);
            }
        }
    }

}


async function fetchData(url) {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return await response.json();
    } catch (error) {
      console.error('There was a problem with your fetch operation:', error);
      throw error; // Re-throw the error to propagate it to the caller
    }
}

function gradeTRTemplate(courseSet) {
    // Course set should include 
    // Course name, code, prereq courses, grade id and grade value

    const tr = document.createElement("tr")

    const td_1 = document.createElement("td")
    td_1.innerText = courseSet.code

    const td_2 = document.createElement("td")
    td_2.innerText= courseSet.name

    const td_3 = document.createElement("td")
    td_3.innerText = courseSet.prereq

    // Grade column
    // Grade column must contain the display itself and in input when edit mode is turned on

    const td_4 = document.createElement("td")
    const td_4_p = document.createElement("p"); // P tag where we display the value
    td_4_p.innerText = courseSet.grade.value
    td_4_p.classList.add('text-center')
    td_4_p.id = `display-${courseSet.id}`

    td_4.appendChild(td_4_p)
    td_4.appendChild(createGradeSelect(courseSet.grade.value, courseSet.id)) // Creating the select option

    const td_5 = document.createElement("td")
    
    const edit_btn = document.createElement("button")
    edit_btn.textContent = "Edit"
    edit_btn.classList.add('btn','btn-primary', 'btn-sm')
    edit_btn.onclick = function() {toggleGradeEditMode(courseSet.id);};
    edit_btn.id = `edit-btn-${courseSet.id}`

    const save_btn = document.createElement("button")
    save_btn.textContent = "Save"
    save_btn.style.display ="none"
    save_btn.classList.add('btn','btn-primary', 'btn-sm')
    save_btn.onclick = function() {saveStudentGrades(courseSet.id);};
    save_btn.id = `save-btn-${courseSet.id}`

    td_5.appendChild(edit_btn);
    td_5.appendChild(save_btn)

    tr.appendChild(td_1);
    tr.appendChild(td_2);
    tr.appendChild(td_3);
    tr.appendChild(td_4);
    tr.appendChild(td_5);

    return tr

}


function gradeTableTemplate(year,sem,courseSets) {
    const headers = ['Course Code', 'Course Name', 'Prerequisite Course', 'Grade', 'Actions']
    const sem_div = document.createElement("div");
    sem_div.classList.add('semester');

    // Table title including year and sem
    const title = document.createElement("h3")
    title.classList.add('semester-title');
    title.innerText = `Year ${year}, Semester: ${sem}`
    sem_div.appendChild(title)

    const table = document.createElement("table");
    table.classList.add('table', 'table-striped');

    const table_head = document.createElement("thead");
    const tr_head = document.createElement("tr");

    // Set up the headers
    headers.forEach(header=> {
        var header_container = document.createElement("th");
        header_container.textContent = header;
        tr_head.appendChild(header_container);
    })

    table_head.appendChild(tr_head)
    
    const table_body = document.createElement("tbody");

    courseSets.forEach(courseSet=> {
        table_body.appendChild(gradeTRTemplate(courseSet))
    })

    table.appendChild(table_head);
    table.appendChild(table_body);
    sem_div.appendChild(table);

    const col = document.createElement("div")
    col.classList.add('col-md-6')

    col.appendChild(sem_div)

    return col

}


function toggleGradeEditMode(course_id) {
    document.getElementById(`edit-btn-${course_id}`).style.display="none"
    document.getElementById(`save-btn-${course_id}`).style.display="block"

    document.getElementById(`display-${course_id}`).style.display="none"
    document.getElementById(`select-${course_id}`).style.display="block"
}


function saveStudentGrades(course_id) {
    // Display related
    document.getElementById(`edit-btn-${course_id}`).style.display="block"
    document.getElementById(`save-btn-${course_id}`).style.display="none"
    document.getElementById(`display-${course_id}`).style.display="block"
    const select = document.getElementById(`select-${course_id}`)
    select.style.display="none"

    // Needs for the post
    // Course id is provided
    // Student profile ID
    // Grade
    const student_id = document.getElementById("pi-id").value
    const grade = select.value

    const data = {
        course_id:course_id,
        student_id:student_id,
        grade: select.value
    };

    const options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: JSON.stringify(data)
    };

    const url = "http://localhost:8000/faculties/student_profiles/grades/update/"
    fetch(url, options)
    .then(response => {
        if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
            alert("Cannot process events now! Try again later.");
        }
        return response.json(); // Parse the JSON response
    })
    .then(data => {
        console.log(data)
        // Update display
        document.getElementById(`display-${course_id}`).innerText = data.grade

    })
    .catch(error => {
        console.log(error)
        alert("Cannot process! Try again later.")
    });
    
}

function createGradeSelect(selected_value,id) {
    const values = [
        "1.00",
        "1.25",
        "1.50",
        "1.75",
        "2.00",
        "2.25",
        "2.50",
        "2.75",
        "3.00",
        "4.00",
        "5.00",
        "INC/5.00"
    ]
    var newSelect = document.createElement('select');
    newSelect.classList.add('form-select')
    newSelect.style.width = "100px";
    newSelect.id = `select-${id}`
    newSelect.style.display = "none"


    values.forEach(value=>{
        var option = document.createElement('option');
        option.value = value;
        option.textContent = value;
        if (selected_value == value) {
            option.selected = true;
        }
        newSelect.appendChild(option);
    })

    return newSelect
}

