// get partner details
function get_partner_details(value) {
    console.log(value, stage_id);
    $.post("/crm/get_partner_details", {
        partner_id: value,
    })
        .done(function (response) {

            $("#partner_email-" + stage_id).val(response["partner_email"]);
            $("#partner_phone-" + stage_id).val(response["partner_phone"]);
        })
        .fail(function () {
            alert("Get Partner Details Error");
        });
}

function get_attribute_values() {
    $.get("/get_attribute_values", function (data) {
        attribute_values = data;

        for (var i = 0; i < data.length; i++) {
            attributes.indexOf(data[i]["attribute_id"]) == -1
                ? attributes.push(data[i]["attribute_id"])
                : null;
        }

        for (var i = 0; i < attributes.length; i++) {
            var result = data.filter((obj) => {
                return obj.attribute == attributes[i];
            });

            autocomplete(document.getElementById("inp-" + attributes[i]), result);
        }
        return attribute_values;
    });
}


// get product description
function get_product_purchase_details(product) {
    $.post("/get_product_purchase_details", {
        product: product,
    })
        .done(function (response) {
            if (
                current_href
                    .toLowerCase()
                    .indexOf("purchase/new/request-for-quotation") >= 0
            ) {
                count_tr = $("#purchase_body").find("tr").length;
                current_index = parseInt(count_tr) - 1;
                document.getElementsByClassName("inp_products")[current_index].id =
                    "product-" + response["id"];
                $("#product-" + response["id"]).css("display", "none");
                // $(".clone-product-tr").attr("id", response["id"] + "-product-tr");
                var product_span = document.createElement("span");
                product_span.innerHTML = response["name"];
                $(product_span).attr("id", "product-span-" + response["id"]);
                document.getElementsByClassName("inp_quantity")[current_index].id =
                    "quantity-for-" + response["id"];
                document.getElementsByClassName("inp_product_desc")[current_index].id =
                    "inp-desc-for-" + response["id"];
                document.getElementsByClassName("product_description")[
                    current_index
                ].id = "desc-for-" + response["id"];
                document.getElementsByClassName("inp_uom")[current_index].id =
                    "uom-for-" + response["id"];
                document.getElementsByClassName("inp_unit_price")[current_index].id =
                    "unit-price-for-" + response["id"];
                document.getElementsByClassName("sub_total")[current_index].id =
                    "sub-total-for-" + response["id"];
                $("#inp-desc-for-" + response["id"]).val(response["description"]);
                $("#unit-price-for-" + response["id"]).val(response["unit_price"]);
                $("#quantity-for-" + response["id"]).val("1.00");
                document.getElementById("sub-total-for-" + response["id"]).innerHTML =
                    insertCommas(response["unit_price"]);

                current_total = document.getElementsByClassName("total")[0].innerHTML;
                new_total =
                    parseInt(removeComma(current_total)) +
                    parseInt(removeComma(response["unit_price"]));
                document.getElementsByClassName("total")[0].innerHTML =
                    insertCommas(new_total);
                // $("#desc-for-" + response["id"]).text(response['description']);
                td_product =
                    document.getElementsByClassName("td_product")[current_index];
                $(product_span).appendTo($(td_product));
                $(td_product).removeClass("w-25");
                $.get("/get_UOM", function (data) {
                    autocomplete(
                        document.getElementsByClassName("inp_uom")[current_index],
                        data
                    );
                    return data;
                });
            }
        })
        .fail(function () { });
}