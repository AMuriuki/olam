// new crm pipeline item
$(".frm-new-item").submit(function (e) {
    e.preventDefault();
    var form = $(this);
    var url = form.attr('action');
    // get form id
    var form_id = form.attr('id');
    var stage_id = getId(form_id);

    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: function (response) {
            if (response['message'] == "success") {
                var clone = $("#clone-" + stage_id).clone()
                $(clone).attr('id', 'item-' + response['opportunity_id']);
                $(clone).find('.opportunity-name').text(response['opportunity_name']);
                $(clone).find('.opportunity-link').attr('href', '/crm/lead/' + response['opportunity_slug']);
                $(clone).find('.edit-opportunity-link').attr('href', '/crm/edit/lead/' + response['opportunity_slug']);
                $(clone).find('.currency').text(response['currency']);
                $(clone).find('.expected-revenue').text(response['expected_revenue']);
                $(clone).find('.partner').text(response['partner_name']);
                var priority = response['priority'];
                if (priority == "1") {
                    $(clone).find(".priority-2").hide();
                    $(clone).find(".priority-3").hide();
                } else if (priority == "2") {
                    $(clone).find(".priority-1").hide();
                    $(clone).find(".priority-3").hide();
                } else if (priority == "3") {
                    $(clone).find(".priority-1").hide();
                    $(clone).find(".priority-2").hide();
                }
                $(clone).find('.agent').text(response['agent_name']);
                $(clone).find('.agent').css('background-color', response['color_badge']);
                $(clone).find('.agent').css('border-color', response['color_badge']);
                $(clone).removeClass('clone');
                $("#new_item-" + stage_id).after($(clone));
                $(".count-" + stage_id).text(response['count']);
                $(form)[0].reset();
                $("#new_item-" + stage_id).fadeOut("slow");
            } else {
                alert(response['message']);
            }
        }
    })

})

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
    if ($(".product-name").val()) {
        $("#modalLoading").modal("show");
        var form = $("#new_product");
        var formData = new FormData(form[0]);
        var fileInput = document.querySelector("#product_image");
        selectedFiles = fileInput.files;

        selectedFiles.forEach((file) => {
            formData.append("files", file)
        });
        var url = form.attr("action")

        $.ajax({
            type: "POST",
            processData: false,
            contentType: false,
            cache: false,
            url: url,
            data: formData,
            success: function (data) {
                // location.href = "/inventory/product/" + data["product_id"];
            }
        })
    } else {
        $(".prod-name-error").text("* Provide a name for your product")
    }

})

// preview product on website
$(".preview-on-website").click(function (e) {
    e.preventDefault();

    if ($(".product-name").val()) {
        $(".preview-mode").prop('checked', true);
        $("#modalLoading").modal("show");
        var form = $("#new_product");
        var url = form.attr("action")
        $.ajax({
            type: "POST",
            url: url,
            data: form.serialize(),
            success: function (data) {
                url = "http://127.0.0.1:5000/preview/" + data["category_slug"] + "/" + data["product_id"]
                window.open(url, '_blank').focus();
            }
        })
    } else {
        $(".prod-name-error").text("* Provide a name for your product")
    }
})

// edit product
$(".edit-product").click(function (e) {
    e.preventDefault();
    $("#modalLoading").modal("show");
    var form = $("#new_product");
    var formData = new FormData(form[0]);
    var fileInput = document.querySelector("#product_image");
    selectedFiles = fileInput.files;
    selectedFiles.forEach((file) => {
        formData.append("files", file)
    })
    var url = form.attr("action")
    $.ajax({
        type: "POST",
        processData: false,
        contentType: false,
        cache: false,
        url: url,
        data: formData,
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
        matched = true;
        $("#hidden" + inp_id).val(response['key']);
    })
}


function create_partner(partner) {
    $.post("/contacts/create_partner", {
        partner: partner
    }).done(function (response) {
        partner_slug = response['slug'];
        partner_id = response['id'];
        $("#partner_id").val(partner_id);
        if (current_href.toLowerCase().indexOf("crm/index") >= 0) {
            get_partner_details(partner_slug);
        }
    }).fail(function (xhr) {
        if (xhr.status == 403) {
            alert("You are not authorized to create a partner. Contact your site administrator for more information.");
        }
    })
}


function create_plan(plan) {
    $.post("/settings/create_plan", {
        plan: plan
    }).done(function (response) {
        $("#plan_id").val(response['id']);
    }).fail(function (xhr) {
        if (xhr.status == 403) {
            alert("You are not authorized to create a plan. Contact your site administrator for more information.");
        }
    })
}


// post opportunity priority
function select_priority(value) {
    $.post("/crm/selected_priority", {
        selected_priority: value,
    })
        .done(function (response) { })
        .fail(function () { });
}


function delete_lead(id) {
    $.post("/crm/delete/lead", {
        lead_id: id,
    }).done(function (response) {
        $("#confirmDelete").modal("hide");
        $("#item-" + id).fadeOut("slow")
        $(".count-" + response['stage_id']).text(response['stage_count'])
    });
}

function update_stage(lead_id, new_stage, prev_stage) {
    console.log(lead_id, new_stage, prev_stage);
    $.post("/crm/update/stage", {
        lead_id: lead_id,
        new_stage: new_stage,
        prev_stage: prev_stage,
    }).done(function (response) {
        $(".count-" + prev_stage).text(response['prev_count']);
        $(".count-" + new_stage).text(response['new_count']);
    });
}


function clear_pipeline_filter(filter_name) {
    $.post("/crm/index", {
        clear_filter_name: filter_name,
    }).done(function (response) {
        // remove all items
        $(".pipeline-item").remove();

        // get length of response
        var length = response["pipeline"]["items"].length;
        var item = response["pipeline"]["items"];
        var stages = []
        // loop through response
        for (var i = 0; i < length; i++) {
            stages.push(item[i]["stage"])
            const counts = {}
            for (const num of stages) {
                counts[num] = counts[num] ? counts[num] + 1 : 1;
            }
            var stage_count = counts[item[i]["stage"]]

            var clone = $("#clone-" + item[i]['stage']).clone()
            $(clone).attr('id', 'item-' + item[i]['id']);
            $(clone).find('.opportunity-name').text(item[i]['opportunity_name']);
            $(clone).find('.opportunity-link').attr('href', '/crm/lead/' + item[i]['opportunity_slug']);
            $(clone).find('.edit-opportunity-link').attr('href', '/crm/edit/lead/' + item[i]['opportunity_slug']);
            $(clone).find('.currency').text(item[i]['currency']);
            $(clone).find('.expected-revenue').text(item[i]['expected_revenue']);
            $(clone).find('.partner').text(item[i]['partner_name']);
            var priority = item[i]['priority'];
            if (priority == "1") {
                $(clone).find(".priority-2").hide();
                $(clone).find(".priority-3").hide();
            } else if (priority == "2") {
                $(clone).find(".priority-1").hide();
                $(clone).find(".priority-3").hide();
            } else if (priority == "3") {
                $(clone).find(".priority-1").hide();
                $(clone).find(".priority-2").hide();
            }
            $(clone).find('.agent').text(item[i]['assignee_name']);
            $(clone).find('.agent').css('background-color', item[i]['color_badge']);
            $(clone).find('.agent').css('border-color', item[i]['color_badge']);
            $("#new_item-" + item[i]['stage']).after($(clone));
            $(".count-" + item[i]['stage']).text(stage_count);
            $(clone).fadeIn("slow");

        }
    });
}