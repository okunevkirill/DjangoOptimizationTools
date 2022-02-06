window.onload = function () {

    $('.ajax_change select').change(function () {
        let lang = document.getElementById("language_site")
        lang.type = "submit";
        $('#language_site').trigger('click');
        lang.type = "hidden";
    });

    $('.orders_list').on('change', 'select', function (event) {
        let item = event.target
        $.ajax(
            {
                url: "/admins/order/" + item.name + "/" + "edit/" + item.value + "/",
                data: 'csrfmiddlewaretoken={{csrf_token}}',
                success: function (data) {
                    $('.orders_list').html(data.result)
                },
            });
        event.preventDefault();
    });
}
