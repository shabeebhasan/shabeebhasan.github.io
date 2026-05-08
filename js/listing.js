(function () {
  function escapeHtml(text) {
    if (!text) return "";
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function createCard(item, ctaLabel) {
    var title = escapeHtml(item.title || "Untitled");
    var excerpt = escapeHtml(item.excerpt || "");
    var image = escapeHtml(item.image || "/assets/imgs/IMG_7856.JPG");
    var url = escapeHtml(item.url || "#");
    return (
      '<article class="studio-card">' +
      '<img src="' + image + '" alt="' + title + '">' +
      '<div class="studio-card-body">' +
      "<h3>" + title + "</h3>" +
      "<p>" + excerpt + "</p>" +
      '<a href="' + url + '" class="btn btn-primary btn-rounded">' + ctaLabel + "</a>" +
      "</div></article>"
    );
  }

  function renderPagination(container, totalPages, currentPage, onPageChange) {
    if (!container) return;
    if (totalPages <= 1) {
      container.innerHTML = "";
      return;
    }
    var html = "";
    for (var i = 1; i <= totalPages; i += 1) {
      html +=
        '<button class="page-btn' +
        (i === currentPage ? " active" : "") +
        '" data-page="' +
        i +
        '">' +
        i +
        "</button>";
    }
    container.innerHTML = html;
    var btns = container.querySelectorAll(".page-btn");
    btns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var page = Number(btn.getAttribute("data-page"));
        if (!page || page === currentPage) return;
        onPageChange(page);
      });
    });
  }

  function initListing(config) {
    var grid = document.getElementById(config.gridId);
    var pager = document.getElementById(config.pagerId);
    var countNode = document.getElementById(config.countId);
    var filterNode = document.getElementById(config.filterId);
    if (!grid) return;

    fetch(config.dataUrl)
      .then(function (r) {
        if (!r.ok) throw new Error("Failed to load listing data.");
        return r.json();
      })
      .then(function (data) {
        var items = Array.isArray(data.items) ? data.items : [];
        var category = "all";
        var page = 1;
        var pageSize = config.pageSize || 9;

        function getFiltered() {
          if (category === "all") return items;
          return items.filter(function (item) {
            return (item.category || "").toLowerCase() === category;
          });
        }

        function render() {
          var filtered = getFiltered();
          var totalPages = Math.max(1, Math.ceil(filtered.length / pageSize));
          if (page > totalPages) page = 1;
          var start = (page - 1) * pageSize;
          var pageItems = filtered.slice(start, start + pageSize);
          grid.innerHTML = pageItems
            .map(function (item) {
              return createCard(item, config.ctaLabel || "Read More");
            })
            .join("");

          if (countNode) {
            countNode.textContent = filtered.length + " results";
          }
          renderPagination(pager, totalPages, page, function (p) {
            page = p;
            render();
          });
        }

        if (filterNode) {
          var btns = filterNode.querySelectorAll("[data-category]");
          btns.forEach(function (btn) {
            btn.addEventListener("click", function () {
              btns.forEach(function (b) { b.classList.remove("active"); });
              btn.classList.add("active");
              category = (btn.getAttribute("data-category") || "all").toLowerCase();
              page = 1;
              render();
            });
          });
        }

        render();
      })
      .catch(function () {
        grid.innerHTML = "<p>Could not load content.</p>";
      });
  }

  window.ListingUI = { initListing: initListing };
})();
