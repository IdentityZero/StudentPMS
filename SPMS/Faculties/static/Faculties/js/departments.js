// Departments Related

// Create new Department
document.getElementById("new-department-form").addEventListener('submit', async function(e){
    e.preventDefault();
    const btn = document.getElementById("new-department-button")
    btn.disabled = true
    btn.textContent = "Adding..."
    const modal = document.getElementById("newDepartmentModal")
    const modalCls = modal.querySelector(".btn-close");


    const department_name = document.getElementById("new-department-input").value

    const url = "http://localhost:8000/faculties/departments/add/"

    const data = {
        department_name:department_name
    }

    try {
        const responseData = await postData(url, data);
        console.log(responseData)
        if ('error' in responseData) {
            alert(responseData.error)
        } else {
            alert("New Department Added")
            modalCls.click()
            department_name.value = ""

        }
    } catch (error) {
        alert("There was a problem processing this request! Try again later.")
    }
    btn.disabled = false
    btn.textContent = "Add"

})


document.getElementById('departmentList').addEventListener('click', async function(e) {
    if (e.target && e.target.matches('a.list-group-item')) {
        const selectedId = parseInt(e.target.getAttribute('data-id'));
        console.log(selectedId)
        const url = `http://localhost:8000/faculties/departments/detail/?id=${selectedId}`
        const container = document.getElementById("degree-container")
        container.innerHTML = ""
        
        const data = await fetchData(url)
        const degrees = data.result.degrees

        document.getElementById('deptTitle').innerText = data.result.department_name;

        degrees.forEach(d=>{
          container.appendChild(degreeSublistTemplate(d.degree_name, d.curriculums))

        })

        document.querySelectorAll('.list-group-item').forEach(item => item.classList.remove('active'));
        e.target.classList.add('active');
        
    }
});


function degreeSublistTemplate(degree, curriculums) {
  const li = document.createElement("li")
  li.classList.add("list-group-item")
  li.textContent = degree

  const ul = document.createElement("ul")
  ul.classList.add("list-group", "subcategory-list")

  curriculums.forEach(curriculum =>{
    let li_sub = document.createElement("li")
    li_sub.textContent = curriculum.curriculum_name
    li_sub.classList.add("list-group-item")
    ul.appendChild(li_sub)
  })

  li.appendChild(ul)

  return li


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

async function postData(url, data) {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
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