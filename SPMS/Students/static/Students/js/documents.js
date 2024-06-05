const documentDelBtn = document.querySelectorAll('button[name="del-doc-btn"]')

documentDelBtn.forEach(btn =>{
    btn.addEventListener('click', () => deleteDocument(btn.id))
})


function deleteDocument (doc_id) {
    const btn = document.getElementById(doc_id)
    const url = "http://localhost:8000/students/documents/delete/"

    const data = { doc: doc_id };
    
    btn.disabled = true;
    btn.textContent = "Deleting...";

    fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          console.log(data); // Handle the response data
          alert('Document deleted successfully');
          window.location.reload();
        })
        .catch(error => {
          console.error('There was a problem with your fetch operation:', error);
          alert('Cannot do this process right now! Try again later')
        });
}


document.addEventListener('DOMContentLoaded', function () {
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[title]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    console.log(tooltipTriggerEl)
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })
});
