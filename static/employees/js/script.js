// Toggle employee subordinates:
$(".card").click(function(event) {
    event.stopPropagation();

    let nestedList = $(this).siblings("ul").first();
    console.log(nestedList)
    if (nestedList.length) {
        let icon = $(this).find(".plus").first().children().first();
        nestedList.toggleClass("d-none d-flex");
        icon.toggleClass("fa-plus fa-minus");
    }
})
