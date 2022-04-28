$(".add-line").on("click", function (e) {
    e.preventDefault();
    count_tr = $(".tbody").find("tr").length;
    current_index = parseInt(count_tr) - 1
    if (current_href.toLowerCase().indexOf("purchase/new/request-for-quotation") >= 0) {
        if ($(".clone-product-tr").length) {
            var inp_quantity_id = $(".inp_quantity:last").attr("id")
            var uom_id = $(".inp_uom:last").attr("id")
            var unit_price_id = $(".inp_unit_price:last").attr("id")
            if (inp_quantity_id) {
                var quantity = document.getElementById(inp_quantity_id)
                var quantity_span = document.createElement("span");
                quantity_span.innerHTML = quantity.value;
                td_quantity = document.getElementsByClassName("td_quantity")[current_index];
                $(quantity_span).appendTo($(td_quantity))
                $(quantity).css("display", "none")
            }
            if (uom_id) {
                var uom = document.getElementById(uom_id)
                var uom_span = document.createElement("span");
                uom_span.innerHTML = uom.value;
                td_uom = document.getElementsByClassName("td_uom")[current_index];
                $(uom_span).appendTo($(td_uom))
                $(uom).css("display", "none")
            }
            if (unit_price_id) {
                var unit_price = document.getElementById(unit_price_id)
                var unit_price_span = document.createElement("span");
                unit_price_span.innerHTML = insertCommas(unit_price.value);
                var product_id = unit_price_id //EXTRACT ID
                unit_price_span.id = "unit-price-span-for-" + product_id
                td_unit_price = document.getElementsByClassName("td_unit_price")[current_index];
                $(unit_price_span).appendTo($(td_unit_price))
                $(unit_price).css("display", "none")
            }
            if ($(".clone-product-tr:last").attr("id")) {
                var clone = $(".og-product-tr").clone();
                $(clone).addClass("clone-product-tr");
                $(clone).removeClass("og-product-tr");
                $(clone).appendTo("#purchase_body");
                count_tr = $("#purchase_body").find("tr").length;
                current_index = parseInt(count_tr) - 1
                $(clone).attr("id", "product-tr-" + count_tr);	//ADD ID
                $.get("/get_products", function (data) {
                    autocomplete(document.getElementsByClassName("inp_products")[current_index], data)
                    return data;
                });
            }
        } else {
            var clone = $(".og-product-tr").clone();
            $(clone).addClass("clone-product-tr");
            $(clone).removeClass("og-product-tr");
            $(clone).appendTo("#purchase_body");
            count_tr = $(".tbody").find("tr").length;
            current_index = parseInt(count_tr) - 1
            $(clone).attr("id", "product-tr-" + current_index);	//ADD ID
            $.get("/get_products", function (data) {
                autocomplete(document.getElementsByClassName("inp_products")[current_index], data)
                return data;
            });
        }
    } else if (current_href.toLowerCase().indexOf("inventory/new/product") >= 0) {
        if ($(".clone-attribute-tr").length) {
            if ($(".inp_attribute:last").val() && $(".inp_value:last").val()) {
                var attribute = $(".inp_attribute:last").val()
                var attribute_span = document.createElement("span");
                attribute_span.innerHTML = attribute;
                attribute_span.id = "attribute-span-for-" + count_tr
                td_attribute = document.getElementsByClassName("td_attribute")[current_index];
                $(attribute_span).appendTo($(td_attribute))
                $(".inp_attribute:last").css("display", "none")

                var value = $(".inp_value:last").val()
                var value_span = document.createElement("span");
                value_span.innerHTML = value;
                value_span.id = "span-attribute-" + count_tr
                td_value = document.getElementsByClassName("td_value")[current_index];
                $(value_span).appendTo($(td_value))
                $(".inp_value:last").css("display", "none")
                $(".form-icon-right:last").css("display", "none")
            }
            if ($("#attribute-span-for-" + count_tr).length && $("#span-attribute-" + count_tr).length) {
                var clone = $(".og-attribute-tr").clone();
                $(clone).addClass("clone-attribute-tr");
                $(clone).removeClass("og-attribute-tr");
                $(clone).appendTo("#attributes_body");
                $(clone).attr("id", "attribute-tr-" + count_tr);	//ADD ID
                document.getElementsByClassName("inp_attribute")[count_tr].id = "input-attribute-" + count_tr
                document.getElementsByClassName("inp_value")[count_tr].id = "input-value-" + count_tr
                $.get("/get_product_attributes", function (data) {
                    type = "product_attributes"
                    autocomplete(document.getElementsByClassName("inp_attribute")[count_tr], data)
                });
            }
        } else {
            var clone = $(".og-attribute-tr").clone();
            $(clone).addClass("clone-attribute-tr");
            $(clone).removeClass("og-attribute-tr");
            $(clone).appendTo("#attributes_body");
            $(clone).attr("id", "attribute-tr-" + count_tr);	//ADD ID
            document.getElementsByClassName("inp_attribute")[count_tr].id = "input-attribute-" + count_tr
            document.getElementsByClassName("inp_value")[count_tr].id = "input-value-" + count_tr
            $.get("/get_product_attributes", function (data) {
                type = "product_attributes"
                autocomplete(document.getElementsByClassName("inp_attribute")[count_tr], data)
                return data;
            });
        }
    }
})