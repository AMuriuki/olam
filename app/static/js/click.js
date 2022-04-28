document.addEventListener('click', function (event) {
    var arr = data
    var values = []
    var isClickInside = null
    var el;
    if (current_href.toLowerCase().indexOf("purchase/new/request-for-quotation") >= 0) {
        el = $(event.target).closest('tr')
        if (el.hasClass('is-click-inside') || $(event.target).hasClass("is-click-inside") || $(event.target).hasClass("add-a-product") || $(event.target).hasClass('select2-selection__rendered') || $(event.target).hasClass('select2-selection__arrow')) {
            isClickInside = true
        }
        if (!isClickInside) {
            $(".clone-product-tr").each(function (i, e) {
                if ($(e).attr("id")) {
                    count_tr = $("#purchase_body").find("tr").length;
                    current_index = parseInt(count_tr) - 1
                    var quantity_el = document.getElementsByClassName("inp_quantity")[current_index];
                    var quantity = quantity_el.value
                    $(quantity_el).css("display", "none");
                    var quantity_span = document.createElement("span");
                    quantity_span.innerHTML = quantity;
                    td_quantity = document.getElementsByClassName("td_quantity")[current_index];
                    $(quantity_span).appendTo($(td_quantity))
                } else {
                    $(e).remove()
                }
            })
        }
    }
    if (current_href.toLowerCase().indexOf("inventory/new/product") >= 0) {
        el = $(event.target)
        if (type == "product_attributes") {
            var val = $(".inp_attribute:last").val()
            $.each(arr, function () {
                var key = Object.keys(this)[0];
                values.push(this[key])
            })
            if ($(el).attr("id") != $(".inp_attribute:last").attr("id")) {
                if (val) {
                    if (values.includes(val)) {
                        console.log("found")
                    } else {
                        $(".inp_attribute:last").val(values[0])
                    }
                }
            }
        }

        if (type = "product_attributes_values") {
            var val = $(".inp_value:last").val()
            $.each(arr, function () {
                var key = Object.keys(this)[0];
                values.push(this[key])
            })
            if ($(el).attr("id") != $(".inp_value:last").attr("id")) {
                if (val) {
                    if (values.includes(val)) {
                        console.log("found")
                    } else {
                        $(".inp_value:last").val(values[0])
                    }
                }
            }
        }

        if (el.hasClass('is-click-inside')) {
            isClickInside = true
        }
        if (!isClickInside) {
            if (!$(".inp_attribute:last").val()) {
                $(".clone-attribute-tr:last").remove()
            }
        }
    }
})