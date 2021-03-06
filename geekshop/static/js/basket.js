window.onload = function () {
    $('.basket_list').on('change', 'input[type="number"]', function () {
        let t_href = event.target
        $.ajax(
            {
                url: "/baskets/edit/" + t_href.name + "/" + t_href.value + "/",
                success: function (data) {
                    $('.basket_list').html(data.result)
                },
            });
        event.preventDefault()
    });

    $('.card_add_basket').on('click', 'button[type="button"]', function (event) {
        let t_href = event.target.value
        const divMsg = document.querySelector('div.message-add');
        $.ajax(
            {
                url: "/baskets/add/" + t_href + "/",
                success: function (data) {
                    $('.card_add_basket').html(data.result)

                    // alert('товар добавлен в корзину')
                    function getHeightMsg(event) {
                        return event.clientHeight;
                    }

                    divMsg.style.transform = `translateY(-${180 + getHeightMsg(divMsg)}px)`;
                    setTimeout(function () {
                        //ваши действия
                        divMsg.style.transform = `translateY(-${0}px)`;
                    }, 800);


                },
            });
        event.preventDefault()
        //
    })

    // var csrf = $('meta[name="csrf-token"]').attr('content');
    // $('.card_add_basket').on('click', 'button[type="button"]', function () {
    //     let t_href = event.target.value
    //     $.ajax(
    //         {   type: 'POST',
    //             headers: {"X-CSRFToken": csrf},
    //             url: "/baskets/add/" + t_href + "/",
    //             success: function (data) {
    //                 $('.card_add_basket').html(data.result)
    //                 alert('товар добавлен вы корзину')
    //             },
    //         });
    //     event.preventDefault()
    //
    // })


}
