$(document).ready(function() {
    $(".nav-link").click(function(event) {
        event.preventDefault();

        let pageUrl = $(this).attr("href");

        $.ajax({
            url: pageUrl,
            method: "GET",
            success: function(response) {
            console.log(response)
                $("main").html(response);
                history.pushState(null, "", pageUrl);
                location.reload();
            },
            error: function() {
                $("main".html("Woops! Try to reload this page :("));
            }
        })
    })

    window.onpopstate = function() {
        $.ajax({
            url: location.pathname,
            method: "GET",
            success: function(response) {
                $("main").html(response);
            }
        })
    }
})

// Toggle employee subordinates:
$(document).on("click", ".card", function(event) {
    event.stopPropagation();

    let card = $(this);
    let nestedList = $(this).siblings("ul").first();
    let icon = $(this).find(".plus");
    if (!nestedList.length) return;

    if (nestedList.children().length) {
        nestedList.toggleClass("d-none d-flex");
        icon.toggleClass("fa-plus fa-minus");
    } else {
        // Load more subordinates
        let managerId = $(icon).attr("manager-id");
        icon.toggleClass("fa-plus fa-spinner fa-spin");
        $(this).css("pointer-events", "none");

        $.ajax({
            url: `/employees/${managerId}/subordinates/`,
            type: "GET",
            headers: {"Accept": "text/html"},
            success: function(response) {
                let container = $(`#subordinates_${managerId}`);
                container.append(response);

                icon = card.find(".plus");
                icon.toggleClass("fa-spinner fa-spin fa-minus");
                nestedList.toggleClass("d-none d-flex");
            },
            error: function() {
                icon = card.find(".plus");
                icon.toggleClass("fa-spinner fa-spin fa-exclamation-triangle");
            },
            complete: function() {
                card.css("pointer-events", "auto");
            }
        });
    }
})