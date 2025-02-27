// Toggle employee subordinates:
$(".list-group-item").click(function(event) {
    event.stopPropagation();

    let nestedList = $(this).find("ul").first();
    if (nestedList.length) {
        let icon = $(this).find(".toggle-btn").first().children().first();
        nestedList.toggleClass("d-none d-inline-flex");
        icon.toggleClass("fa-plus fa-minus");
    }
})
