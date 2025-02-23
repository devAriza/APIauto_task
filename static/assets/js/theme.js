(function() {
  "use strict";

  let sidebar = document.querySelector('.sidebar');
  let sidebarToggles = document.querySelectorAll('#sidebarToggle, #sidebarToggleTop');
  
  if (sidebar) {
    
    let collapseEl = sidebar.querySelector('.collapse');
    let collapseElementList = [].slice.call(document.querySelectorAll('.sidebar .collapse'))
    let sidebarCollapseList = collapseElementList.map(function (collapseEl) {
      return new bootstrap.Collapse(collapseEl, { toggle: false });
    });

    for (let toggle of sidebarToggles) {

      toggle.addEventListener('click', function(e) {
        document.body.classList.toggle('sidebar-toggled');
        sidebar.classList.toggle('toggled');

        if (sidebar.classList.contains('toggled')) {
          for (let bsCollapse of sidebarCollapseList) {
            bsCollapse.hide();
          }
        };
      });
    }

    window.addEventListener('resize', function() {
      let vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);

      if (vw < 768) {
        for (let bsCollapse of sidebarCollapseList) {
          bsCollapse.hide();
        }
      };
    });
  }
  
  let fixedNaigation = document.querySelector('body.fixed-nav .sidebar');
  
  if (fixedNaigation) {
    fixedNaigation.on('mousewheel DOMMouseScroll wheel', function(e) {
      let vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);

      if (vw > 768) {
        let e0 = e.originalEvent,
          delta = e0.wheelDelta || -e0.detail;
        this.scrollTop += (delta < 0 ? 1 : -1) * 30;
        e.preventDefault();
      }
    });
  }

  let scrollToTop = document.querySelector('.scroll-to-top');
  
  if (scrollToTop) {
    
    window.addEventListener('scroll', function() {
      let scrollDistance = window.pageYOffset;

      //check if user is scrolling up
      if (scrollDistance > 100) {
        scrollToTop.style.display = 'block';
      } else {
        scrollToTop.style.display = 'none';
      }
    });
  }

  document.addEventListener("DOMContentLoaded", function () {  

    const logoutLink = document.getElementById("aLogout");
    if (logoutLink) {

      logoutLink.addEventListener("click", function (event) {
        event.preventDefault();

        document.cookie = "id_user=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
            
      });
    }
  });

})();