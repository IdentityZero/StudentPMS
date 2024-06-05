function editAnnouncement(id){
    // Get data to edit
    const title = document.getElementById(`d-title-${id}`).textContent;
    const content = document.getElementById(`d-content-${id}`).textContent;
    let active = document.getElementById(`d-active-${id}`).textContent;

    document.getElementById("editAnnouncementSavebutton").setAttribute('data-value', id)

    if (active == "True") {
        active = "yes";
    } else {
        active = "no";
    }

    // Set data to edit

    document.getElementById("title-form").value = title
    document.getElementById("content-form").value = content
    document.getElementById("active-form").value = active

}


document.getElementById("editAnnouncementSavebutton").addEventListener('click', async function(){
    this.disabled = true;
    this.textContent = "Saving..."

    const id = this.getAttribute('data-value')
    const title = document.getElementById("title-form").value
    const content = document.getElementById("content-form").value
    const active = document.getElementById("active-form").value
    
    const data = {
        id:id,
        title:title,
        content:content,
        active:active
    }

    const url = "http://localhost:8000/faculties/announcements/update/"

    try {
        const responseData = await postData(url, data);
        console.log(responseData)
        if ('error' in responseData) {
            alert(responseData.error)
        } else {
            alert("Announcement Updated")
            window.location.reload();

        }
    } catch (error) {
        alert("There was a problem processing this request! Try again later.")
    }
    this.disabled = false
    this.textContent = "Save Changes"

})



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
