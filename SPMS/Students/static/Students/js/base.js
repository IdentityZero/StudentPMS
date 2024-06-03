const shrink_btn = document.querySelector(".shrink-btn");
const active_tab = document.querySelector(".active-tab");
const sidebar_links = document.querySelectorAll(".sidebar-links li");
const currentUrl = window.location.href

shrink_btn.addEventListener("click", () => {
  document.body.classList.toggle("shrink");

  shrink_btn.classList.add("hovered");

  setTimeout(() => {
    shrink_btn.classList.remove("hovered");
  }, 500);
});


updateSideBar()

function updateSideBar() {
    sidebar_links.forEach(link =>{
        link.classList.remove('active-link')
        var linkAnchor = link.getElementsByTagName('a')[0];
        linkAnchor.classList.remove('active');
    })

    if (currentUrl.includes("profile")) {
        sidebar_links[1].classList.add('active-link');
        var linkAnchor = sidebar_links[1].getElementsByTagName('a')[0];
        linkAnchor.classList.add('active')
    } else if (currentUrl.includes("documents")) {
        sidebar_links[2].classList.add('active-link');
        var linkAnchor = sidebar_links[2].getElementsByTagName('a')[0];
        linkAnchor.classList.add('active')
    } else if (currentUrl.includes("grades")) {
        sidebar_links[3].classList.add('active-link');
        var linkAnchor = sidebar_links[3].getElementsByTagName('a')[0];
        linkAnchor.classList.add('active')
    } else {
        sidebar_links[0].classList.add('active-link');
        var linkAnchor = sidebar_links[0].getElementsByTagName('a')[0];
        linkAnchor.classList.add('active')
    }

}


