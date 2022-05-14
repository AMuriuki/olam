// add new company contact
$("#new_company_contact").submit(function (e) {
    e.preventDefault();
    var form = $(this);
    var url = form.attr("action");

    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: function (data) {
            $("#profile-edit").modal("hide");
            $("#newItem1").show();
            $("#pipeline_select_org-" + stage_id).append(
                $("<option>", { value: data["partner_id"], text: data["partner_name"] })
            );
            $("#select_company").append(
                $("<option>", { value: data["partner_id"], text: data["partner_name"] })
            );
            $("#pipeline_select_org-" + stage_id)
                .val(data["partner_id"])
                .change();
        },
    });
});

// add new individual contact
$("#new_individual_contact").submit(function (e) {
    e.preventDefault();
    var form = $(this);
    var url = form.attr("action");

    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: function (data) {
            $("#profile-edit").modal("hide");
            $("#newItem1").show();
            $("#pipeline_select_org-" + stage_id).append(
                $("<option>", { value: data["partner_id"], text: data["partner_name"] })
            );
            $("#pipeline_select_org-" + stage_id)
                .val(data["partner_id"])
                .change();
        },
    });
});

// submit new plan
$("#new_recurring_plan").submit(function (e) {
    e.preventDefault();
    var form = $(this);
    var url = form.attr("action");

    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: function (data) {
            $("#modalNewPlan").modal("hide");
            $("#newItem_" + stage_id).show();
            $("#recurring_plan-" + stage_id).append(
                $("<option>", { value: data["plan_id"], text: data["plan_name"] })
            );
            $("#recurring_plan-" + stage_id)
                .val(data["plan_id"])
                .change();
        },
    });
});

// invite new user
$("#frm_invite").submit(function (e) {
    e.preventDefault();
    // $('#modalLoading').modal('show');
    $("#dv_notification").show();
    $("#dv_notification").text("Sending email invitation...");
    var form = $(this);
    var url = form.attr("action");

    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: function (data) {
            // $('#modalLoading').modal('hide');
            $("#dv_notification").hide();
            if (data["response"] === "success") {
                location.href = "/settings/general_settings";
            } else {
                $("#modalInvite").modal("show");
                $("#spn_invite_error").text(data["response"]["email"]);
            }
        },
    });
});

$(".create-user").click(function (e) {
    e.preventDefault();
    var form = $("#new_user");
    var url = form.attr("action");
    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: function (data) {
            if (data["response"] == "success") {
                window.location = "/settings/users";
            } else if (data["response"] == "user email exists!") {
                alert("A user with this email already exists");
            }
        },
    });
});

$(".edit-user").click(function (e) {
    e.preventDefault();
    var form = $("#edit_user");
    var url = form.attr("action");
    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: function (data) {
            if (data["response"] == "success") {
                window.location = "/settings/user/" + data["slug"];
            } else if (
                data["response"] == "there is a user with this email address!"
            ) {
                alert("There is a user with this email address!");
            }
        },
    });
});

$(".save-new-group").click(function (e) {
    e.preventDefault();
    if ($("#select_app").val() == "default_option") {
        alert("Select an App");
    } else if ($("#group_name").val() == "") {
        alert("Provide a name for this group");
    } else {
        var form = $("#group_details");
        var url = form.attr("action");
        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(),
            success: function (data) {
                if (data["response"] == "group name exists!") {
                    window.location.reload();
                } else if (data["response"] == "success") {
                    location.href = "/settings/group/" + data["slug"];
                }
            },
        });
    }
});

$(".save-group").click(function (e) {
    e.preventDefault();
    if ($("#select_app").val() == "default_option") {
        alert("Select an App");
    } else if ($("#group_name").val() == "") {
        alert("Provide a name for this group");
    } else {
        var form = $("#group_details");
        var url = form.attr("action");
        slug = $(".span-new-group").attr("id");
        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(),
            success: function (data) {
                if (data["response"] == "group name exists!") {
                    location.href = "/settings/edit_group/" + slug;
                } else if (data["response"] == "success") {
                    if (
                        current_href.toLowerCase().indexOf("settings/edit_group") >= 0 ||
                        current_href.toLowerCase().indexOf("settings/new_group/") >= 0
                    ) {
                        location.href = "/settings/group/" + slug;
                    }
                }
            },
        });
    }
});

// add new product
$(".create-product").click(function (e) {
    e.preventDefault();
    $("#modalLoading").modal("show");
    count_tr = $("#attributes_body").find("tr").length - 1;
    $(".number-of-attributes").val(count_tr)
    var form = $("#new_product");
    var url = form.attr("action")
    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: function (data) {
            location.href = "/inventory/product/" + data["product_id"];
        }
    })
})

// edit product
$(".edit-product").click(function (e) {
    e.preventDefault();
    $("#modalLoading").modal("show");
    var form = $("#new_product");
    var url = form.attr("action")
    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: function (data) {
            location.href = "/inventory/product/" + data["product_id"];
        }
    })
})

$(".select-access-group").on("change", function (e) {
    e.preventDefault();
    var group_id = $(this).attr("id");
    current_href = $(location).attr("href");
    $.post(current_href, {
        group_id: group_id,
        checked: $(this).prop("checked")
    })
})

function post_vendor(vendor) {
    if (sessionStorage.getItem('purchase_id')) {
        purchase_id = sessionStorage.getItem('purchase_id');
    } else {
        purchase_id = null;
    }
    $.post("/purchase/new/request-for-quotation", {
        vendor: vendor,
        purchase_id: purchase_id
    }).done(function (response) {
        sessionStorage.setItem('purchase_id', response['purchase_id']);
    })
}


function post_product_attribute_value(attribute, value, id) {
    $.post("/create_product_attribute_value", {
        attribute: attribute,
        value: value
    }).done(function (response) {
        $("#" + id).val(response['key'])
    })
}