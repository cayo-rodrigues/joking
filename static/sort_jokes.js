function sort_jokes(order) {
    // send ajax request to server, so that the jokes
    // will be displayed in the selected order at any profile page
    $.post(`/sort/${order}`, () => {
        // reload just the jokes section
        $(".jokes").load(" .jokes > *");
    });
}