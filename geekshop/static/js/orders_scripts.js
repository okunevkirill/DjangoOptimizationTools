"use strict";

let totalForms, orderTotalQuantity, orderTotalCost;
let $orderTotalQuantityDOM, $orderTotalCostDOM, $orderForm;
let quantity, price, orderItemNum, orderItemQuantity, deltaQuantity;
let quantityArr = [], priceArr = [];


class ValidationError extends Error {
    constructor(message) {
        super(message);
        this.name = "ValidationError";
    }
}

/**
 * Функция получения исходных значений о каждом из товаров в заказе
 */
function parseOrderForm() {
    for (let i = 0; i < totalForms; i++) {
        quantity = parseInt($(`input[name="orderitems-${i}-quantity"]`).val());
        price = parseFloat($(`.orderitems-${i}-price`).text().replace(',', '.'));

        quantityArr[i] = quantity;
        priceArr[i] = price ? price : 0;
    }
}

/**
 * Функция обновления суммарной информации заказа
 * @param orderItemPrice - цена за единицу товара
 * @param deltaQuantity - разница количества товара
 */
function orderSummaryUpdate(orderItemPrice, deltaQuantity) {
    let deltaCost = orderItemPrice * deltaQuantity;
    orderTotalCost = Number(orderTotalCost + deltaCost) || 0;

    orderTotalQuantity = (orderTotalQuantity + deltaQuantity) || 0;

    $orderTotalQuantityDOM.html(`${orderTotalQuantity}`);
    $orderTotalCostDOM.html(`${orderTotalCost.toFixed(2)}`);
}

/**
 * Функция прослушивания для установки новых значений о суммарной
 * информации заказа при изменении количества товаров в заказе
 * @param event - DOM элемент над которым совершили действие
 */
function setOrderSummaryUpdate(event) {
    let target = event.target
    orderItemNum = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
    if (priceArr[orderItemNum]) {
        orderItemQuantity = parseInt(target.value);
        deltaQuantity = orderItemQuantity - quantityArr[orderItemNum];
        quantityArr[orderItemNum] = orderItemQuantity;
        orderSummaryUpdate(priceArr[orderItemNum], deltaQuantity);
    }
}

/**
 * Функция прослушивания для отработки удаления товара целиком
 * @param event - DOM элемент над которым совершили действие
 */
function setOrderItemDelete(event) {
    orderItemNum = parseInt(event.target.name.replace('orderitems-', '').replace('-DELETE', ''));
    if (event.target.checked) {
        deltaQuantity = -quantityArr[orderItemNum];
    } else {
        deltaQuantity = quantityArr[orderItemNum];
    }
    orderSummaryUpdate(priceArr[orderItemNum], deltaQuantity);
}


/**
 * Функция добавления и удаления formset
 * @param row - строка формы над которой производят действие
 */
function deleteOrderItem(row) {
    let targetName = row[0].querySelector('input[type="number"]').name
    orderItemNum = parseInt(targetName.replace('orderitems-', '').replace('-quantity', ''));
    deltaQuantity = -quantityArr[orderItemNum]
    quantityArr[orderItemNum] = 0;
    if (!isNaN(priceArr[orderItemNum]) && !isNaN(deltaQuantity)) {
        orderSummaryUpdate(priceArr[orderItemNum], deltaQuantity);
    }
}


/**
 * Функция прослушивания изменения позиции товара
 * @param event - элемент на который воздействовали
 */
function changeProduct(event) {
    let pkProduct = event.target.value;
    const itemTrParent = event.target.closest('tr');
    if (pkProduct) {
        // Выбран не пустой товар
        $.ajax(
            {
                url: `/orders/product/change/${pkProduct}/`,
                success: function (data) {
                    if (!data.productPrice)
                        throw new ValidationError(`Ошибка запроса ${data.error}`);

                    orderItemNum = parseInt(event.target.name.replace('orderitems-', '').replace('-product')) || 0;
                    let itemPrice = itemTrParent.querySelector(`.td3`);

                    itemPrice.innerHTML = `<span class="orderitems-${orderItemNum}-price">${data.productPrice} руб </span>`;

                    let changeQuantity = itemTrParent.querySelector('input[type="number"]');
                    if (priceArr[orderItemNum]) {
                        orderSummaryUpdate(priceArr[orderItemNum], -quantityArr[orderItemNum]); // Отнимаем старый товар
                    } else {
                        // новый товар
                        changeQuantity.value = 1;
                        quantityArr[orderItemNum] = 1;
                    }
                    priceArr[orderItemNum] = data.productPrice;
                    orderSummaryUpdate(priceArr[orderItemNum], quantityArr[orderItemNum]);

                },
            });
    } else {
        // Выбран пустой товар - ветка удаления
        let btn = itemTrParent.querySelector('.delete-row');
        btn.click();
    }
    event.preventDefault();
}

// ------------------------------------------------------------------------------
/**
 * Основной функционал скрипта
 */
document.addEventListener("DOMContentLoaded", function () {

    $orderTotalQuantityDOM = $('.order_total_quantity');
    $orderTotalCostDOM = $('.order_total_cost');
    $orderForm = $('.order_form');

    orderTotalQuantity = parseInt($orderTotalQuantityDOM.text()) || 0;
    orderTotalCost = parseFloat($orderTotalCostDOM.text().replace(',', '.')) || 0;
    totalForms = parseInt($("input[name='orderitems-TOTAL_FORMS']").val());

    parseOrderForm(); // Парсинг management_form

    $orderForm.on('change', 'input[type=number]', setOrderSummaryUpdate); // Обновление при изменении checkbox

    $orderForm.on('change', 'input[type="checkbox"]', setOrderItemDelete); // Обновление при удалении товара

    // Работа с добавлением новых товаров
    $('.formset_row').formset({
        addText: 'Добавить продукт',
        deleteText: 'Удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem,
    });

    // Отработка изменения товара в formset
    $orderForm.on('change', 'select', changeProduct);
});

