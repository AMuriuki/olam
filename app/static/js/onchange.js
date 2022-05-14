var attribute;
var value;

$(".chk_user").change(function (e) {
    var user_id = $(this).attr("id");
    if (this.checked) {
        selectedUsers.push(user_id);
        selected = selected + 1;
        $(".export").hide();
        $(".selected-groups").show();
        $(".li-actions").show();
        $(".selected-groups").text(selected + " selected");

    } else {
        const index = selectedUsers.indexOf(user_id);
        selectedUsers.splice(index);
        selected = selected - 1;
        if (selected == 0) {
            $(".export").show();
            $(".selected-groups").hide();
            $(".li-actions").hide();
        } else {
            $(".selected-groups").text(selected + " selected");
        }
    }
});


// add new contact
$(".select_contact").on("change", function () {
    stage_id = getId(this.id);
    if (this.value === "add_new") {
        $("#profile-edit").modal("show");
    } else {
        get_partner_details(this.value);
    }
});

$(".set-due-date").on("change", function () {
    var due_date = $(this).val();
    var purchase_id = sessionStorage.getItem('purchase_id');
    $.post("/purchase/new/request-for-quotation", {
        purchase_id: purchase_id,
        due_date: due_date
    }).done(function (response) {
        sessionStorage.setItem('purchase_id', response['purchase_id']);
    })
})

$(".inp_quantity").on("change", function () {
    var quantity = $(this).val();

    var product_id = $(this).attr("id"); //EXTRACT ID
    var unit_price_input = document.getElementById("unit-price-for-" + response['id'])
    var unit_price_span = document.getElementById("unit-price-span-for-" + response['id'])
    if (unit_price_input) {
        var unit_price = unit_price_input.value
    } else if (unit_price_span) {
        var unit_price = unit_price_input.innerHTML
    }
    var new_sub_total = parent(quantity) * parseFloat(unit_price)
    document.getElementById("sub-total-for-" + response['id']).innerHTML = new_sub_total
    var purchase_id = sessionStorage.getItem('purchase_id');
    $.post("/purchase/new/request-for-quotation", {
        purchase_id: purchase_id,
        quantity: quantity
    }).done(function (response) {
        sessionStorage.setItem('purchase_id', response['purchase_id']);
    })
})

$(".set-time").on("change", function () {
    var time = $(this).val();
    var purchase_id = sessionStorage.getItem('purchase_id');
    $.post("/purchase/new/request-for-quotation", {
        purchase_id: purchase_id,
        time: time
    }).done(function (response) {
        sessionStorage.setItem('purchase_id', response['purchase_id']);
    })
})

// add new recurring plan modal
$(".recurring-plan").on("change", function () {
    stage_id = getId(this.id);
    if (this.value === "new_plan") {
        $("#modalNewPlan").modal("show");
    }
});

$("#company").change(function () {
    var text = $(this).val();
    $("#domain").val(text);
});

$("#individual").change(function () {
    if (this.checked) {
        $("#company-block").hide();
        $("#individual-block").show();
    }
});

$("#company").change(function () {
    if (this.checked) {
        $("#individual-block").hide();
        $("#company-block").show();
    }
});

$(".select_country").change(function () {
    country = $(this).val();
    get_city(country);
});

$(".set-access").change(function (e) {
    var group_id = $(this).val();
    var module_id = $(this).attr("id");

    $.post("/settings/set-access", {
        group: group_id,
        module: module_id,
    }).done(function (response) { });
});

$(".record-check").change(function (e) {
    if (this.checked) {
        selected = selected + 1;
        selectedGroups.push(this.id);
        $(".export").hide();
        $(".selected-groups").show();
        $(".li-actions").show();
        $(".selected-groups").text(selected + " selected");
    } else {
        selected = selected - 1;
        const index = selectedGroups.indexOf(this.id);
        selectedGroups.splice(index);
        if (selected == 0) {
            $(".export").show();
            $(".selected-groups").hide();
            $(".li-actions").hide();
        } else {
            $(".selected-groups").text(selected + " selected");
        }
    }
});

$("#add_access_name").change(function () {
    access_name = $(this).val();
    if ($("#select_model").val() != "default_option") {
        $(".submit-access-right")
            .addClass("btn-primary")
            .removeClass("btn-secondary");
    } else if ($(this).val() == "") {
        $(".submit-access-right")
            .addClass("btn-secondary")
            .removeClass("btn-primary");
    }
});

$("#select_model").change(function () {
    selected_model = $(this).val();
    if ($("#add_access_name").val().length != 0) {
        $(".submit-access-right")
            .addClass("btn-primary")
            .removeClass("btn-secondary");
    } else if ($(this).val() == "default_option") {
        $(".submit-access-right")
            .addClass("btn-secondary")
            .removeClass("btn-primary");
    }
});

$("#read_access").change(function () {
    if (this.checked) {
        read = true;
    } else {
        read = false;
    }
});

$(".read_access").change(function () {
    id_of_access_right = $(this).attr("id").split(".")[1];
    if (this.checked) {
        $.post("/settings/access-right", {
            access: id_of_access_right,
            read: true,
        });
    } else {
        $.post("/settings/access-right", {
            access: id_of_access_right,
            read: false,
        });
    }
});

$("#write_access").change(function () {
    if (this.checked) {
        write = true;
    } else {
        write = false;
    }
});

$(".write_access").change(function () {
    id_of_access_right = $(this).attr("id").split(".")[1];
    if (this.checked) {
        $.post("/settings/access-right", {
            access: id_of_access_right,
            write: true,
        });
    } else {
        $.post("/settings/access-right", {
            access: id_of_access_right,
            write: false,
        });
    }
});

$("#create_access").change(function () {
    if (this.checked) {
        create = true;
    } else {
        create = false;
    }
});

$(".create_access").change(function () {
    id_of_access_right = $(this).attr("id").split(".")[1];
    if (this.checked) {
        $.post("/settings/access-right", {
            access: id_of_access_right,
            create: true,
        });
    } else {
        $.post("/settings/access-right", {
            access: id_of_access_right,
            create: false,
        });
    }
});

$("#delete_access").change(function () {
    if (this.checked) {
        _delete = true;
    } else {
        _delete = false;
    }
});

$(".delete_access").change(function () {
    id_of_access_right = $(this).attr("id").split(".")[1];
    if (this.checked) {
        $.post("/settings/access-right", {
            access: id_of_access_right,
            delete: true,
        });
    } else {
        $.post("/settings/access-right", {
            access: id_of_access_right,
            delete: false,
        });
    }
});

$(".update_access_right_name").change(function () {
    name_of_access_right = $(this).val();
    var input_id = $(this).attr("id");
    var el = document.getElementById(input_id);

    $.post("/settings/access-right", {
        name: name_of_access_right,
        access: id_of_access_right,
    }).done(function (response) {
        var span = document.createElement("span");
        span.innerHTML = name_of_access_right;
        span.className = span_access_class;
        insertAfter(el, span);
        $(".update_access_right_name").hide();
    });
});

$(".select_model").change(function () {
    selected_model = $(this).val();
    var div_id = $(this).closest("div").attr("id");
    var el = document.getElementById(div_id);
    $.post("/settings/access-right", {
        access: id_of_access_right,
        model_id: selected_model,
    }).done(function (response) {
        var span = document.createElement("span");
        span.innerHTML = response["model_name"];
        span.className = span_model_class;
        insertAfter(el, span);
        document.getElementById(div_id).style.display = "none";
    });
});

$(".inp_uom").change(function () {
    if (!selected_key) {
        $.post("/get_uom_key", {
            name: $(this).val()
        }).done(function (response) {
            document.getElementById("uom_id").value = response['key'];
        })
    } else {
        document.getElementById("uom_id").value = key;
    }
})

$(".inp_category").change(function () {
    if (!selected_key) {
        $.post("/get_category_key", {
            name: $(this).val()
        }).done(function (response) {
            document.getElementById("category_id").value = response['key'];
        })
    } else {
        document.getElementById("category_id").value = selected_key;
    }
})

$(".inp_products").change(function () {
    get_product_purchase_details(key);
    post_product_purchase(key)
})

$(".inp_vendor").change(function () {
    post_vendor(key);
})

$(".inp_tags").change(function () {
    add_tag(key, value);
})

$(".inp_attribute").change(function () {

})

function handleChange(inp) {
    if ($(inp).hasClass("inp_value")) {
        var span_el = document.createElement("span");
        span_el.innerHTML = $(inp).val();
        span_el.id = "span-attribute-value-" + (inp.id).replace("inp-", "")
        $(span_el).insertAfter($(inp));
        $(inp).attr("hidden", true)
    }
}

$(".inp_value").change(function (e) {
    document.addEventListener('click', function (event) {
        if (!$(event.target).hasClass("create-new-item") || !$(event.target).hasClass("autocomplete-item")) {
            for (item in matching) {
                console.log(matching[item], $(".inp_value").val())
                console.log(matching[item] === $(this).val())
                if ((matching[item]).toLowerCase() === ($(this).val()).toLowerCase()) {
                    console.log(matching[item]);
                }
            }
        }
    })
})


// $(".inp_value").on("change", function () {
//     var this_id = $(this).attr("id");
//     var hidden_id = "hidden-" + this_id
//     document.addEventListener('click', function (event) {
//         $("#" + hidden_id).attr("name", 'attribute-value-input-' + this_id.replace("inp-", ""));
//         var span_el = document.createElement("span");
//         span_el.id = "span-attribute-value-" + this_id
//         if ($(event.target).closest("div").hasClass("autocomplete-item")) {
//             selected_value = $(event.target).text()
//         } else if ($(event.target).closest("div").hasClass("create-new-item")) {
//             selected_value = ($(event.target).text()).replace("Create ", "")
//         } else {
//             if ($(".inp_value").val()) {
//                 if (confirm('Create new attribute value ' + $("#" + this_id).val())) {
//                     selected_value = $("#" + this_id).val();
//                 } else {
//                     value = $("#" + this_id).val();
//                     span_el.innerHTML = value
//                 }
//             }
//         }
//         if (!selected_key) {
//             if (selected_value) {
//                 $.post("/get_attribute_value_key", {
//                     name: selected_value,
//                     attribute: this_id.replace("inp-", "")
//                 }).done(function (response) {
//                     $("#" + hidden_id).val(response['key']);
//                 })
//                 span_el.innerHTML = selected_value
//             }
//         } else {
//             $("#" + hidden_id).val(selected_key);
//         }
//         var exists = document.getElementById("span-attribute-value-" + this_id)
//         if (!exists) {
//             $(span_el).insertAfter($("#" + this_id));
//         }
//         $("#" + this_id).attr("hidden", true);
//     })
// })

document.addEventListener('change', function (event) {
    count_tr = $("#purchase_body").find("tr").length;
    current_index = parseInt(count_tr) - 1
    if (event.target == document.getElementsByClassName("inp_quantity")[current_index]) {
        var quantity_el = document.getElementsByClassName("inp_quantity")[current_index];
        var quantity = quantity_el.value
        var unit_price_el = document.getElementsByClassName("inp_unit_price")[current_index];
        var unit_price = unit_price_el.value
        var sub_total_el = document.getElementsByClassName("sub_total")[current_index];
        var sub_total = quantity * unit_price
        sub_total_el.innerHTML = insertCommas(sub_total)
        var total = 0
        for (i = 0; i < count_tr; i++) {
            var sub_total_el = document.getElementsByClassName("sub_total")[i];
            var sub_total = sub_total_el.innerHTML
            total += parseInt(sub_total.replace(/,/g, ""))
        }
        var total_el = document.getElementsByClassName("total")[0];
        var total = insertCommas(total)
        total_el.innerHTML = total
    }
})