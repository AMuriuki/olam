document.addEventListener("click", function (event) {
    var el = $(event.target);
    if (el.hasClass("span-attribute-value")) {
        var td_el = el.parent();
        var attribute_id = el.attr("id").replace("span-attribute-value-", "");
        var inp_id = "inp-" + attribute_id;
        $(td_el).append(
            '<input id="' +
            inp_id +
            '" class="form-control inp_value is-click-inside" value="' +
            $(el).text() +
            '">'
        );
        $(el).remove();
        selected_key = null;

        var result = attribute_values.filter((obj) => {
            return obj.attribute == attribute_id;
        });

        autocomplete(document.getElementById(inp_id), result);
    }

    if (!el.hasClass('is-click-inside')) {
        closeAllLists();
    }
});


// add new board item
$(".add-item").click(function (e) {
    e.preventDefault();
    stage_id = getId(this.id);
    $("#new_item-" + stage_id).fadeIn("slow");
    $("#new_item-" + stage_id)[0].scrollIntoView({
        behavior: "smooth", // or "auto" or "instant"
        block: "start" // or "end"
    });
    pipeline_stage(stage_id);
});

$(".schedule").click(function (e) {
    record_id = this.id;
    $.post("/crm/get_opportunityID", {
        opportunity_id: record_id,
    }).done(function (response) { });
    $(".record_id").attr("id", record_id);
});

$(".edit-stage").click(function (e) {
    e.preventDefault();
    stage_id = this.id;
    $("#modalEditStage").modal("show");
});

$(".delete-stage").click(function (e) {
    e.preventDefault();
    stage_id = this.id;
    $("#confirmDelete").modal("show");
});

$("#deleteStage").click(function (e) {
    delete_stage();
});

$(".move-stage-forward").click(function (e) {
    e.preventDefault();
    stage_id = this.id;
    move_stage_forward();
});

$(".move-stage-behind").click(function (e) {
    e.preventDefault();
    stage_id = this.id;
    move_stage_behind();
});

// handle edit stage submit event
$("#submit_stage_edits").click(function (e) {
    e.preventDefault();
    stage_name = $("#stage_name").val();
    $("#stage_title_" + stage_id).html(stage_name);
    edit_stage();
});

$(".select-priority").click(function (e) {
    e.preventDefault();
    var el, el2, el3;
    var value;
    item_id = this.name;
    el = $("#priority1-" + item_id);
    el2 = $("#priority2-" + item_id);
    el3 = $("#priority3-" + item_id);

    if (this.id === "selectPriority1-" + item_id) {
        if (el.hasClass("asterisk-off")) {
            el.removeClass("asterisk-off");
            el.removeClass("ni-star");
            el.addClass("ni-star-fill");
            value = 1;
        } else {
            el.removeClass("ni-star-fill");
            el.addClass("asterisk-off");
            el.addClass("ni-star");
            el2.removeClass("ni-star-fill");
            el2.addClass("asterisk-off");
            el2.addClass("ni-star");
            el3.removeClass("ni-star-fill");
            el3.addClass("asterisk-off");
            el3.addClass("ni-star");
            value = 0;
        }
    } else if (this.id === "selectPriority2-" + item_id) {
        if (el2.hasClass("asterisk-off")) {
            el.removeClass("asterisk-off");
            el.removeClass("ni-star");
            el.addClass("ni-star-fill");
            el2.removeClass("asterisk-off");
            el2.removeClass("ni-star");
            el2.addClass("ni-star-fill");
            value = 2;
        } else {
            el2.removeClass("ni-star-fill");
            el2.addClass("asterisk-off");
            el2.addClass("ni-star");
            el3.removeClass("ni-star-fill");
            el3.addClass("asterisk-off");
            el3.addClass("ni-star");
            value = 1;
        }
    } else if (this.id === "selectPriority3-" + item_id) {
        if (el3.hasClass("asterisk-off")) {
            el.removeClass("asterisk-off");
            el.removeClass("ni-star");
            el.addClass("ni-star-fill");
            el2.removeClass("asterisk-off");
            el2.removeClass("ni-star");
            el2.addClass("ni-star-fill");
            el3.removeClass("asterisk-off");
            el3.removeClass("ni-star");
            el3.addClass("ni-star-fill");
            value = 3;
        } else {
            el3.removeClass("ni-star-fill");
            el3.addClass("asterisk-off");
            el3.addClass("ni-star");
            value = 2;
        }
    }
    select_priority(value);
});

$(".filter-users").click(function (e) {
    e.preventDefault();
    filter_id = $(this).attr("id");
    var filter_name = $(this).children("span").text();

    if (hasClass($(this).children("em"), "ni-check-thick")) {
        const index = selectedFilters.indexOf(filter_id);
        selectedFilters.splice(index, 1);
        $(this).children("em").removeClass("ni-check-thick");
        var current_value = $("#search_users").val();
        if (current_value == "All Users") {
            new_value = current_value.replace("All Users" + ",", "");
        } else {
            new_value = current_value.replace(filter_name + ",", "");
        }
        $("#search_users").val(new_value);
        if (new_value) {
            location.href = "/settings/users?filter=" + new_value;
        } else {
            location.href = "/settings/users?filter=" + "All Users";
        }
    } else {
        selectedFilters.push(filter_id);
        $(this).children("em").addClass("ni-check-thick");
        var current_value = $("#search_users").val();
        if (current_value == "All Users") {
            new_value = current_value.replace("All Users", filter_name + ", ");
        } else {
            new_value = current_value + filter_name + ", ";
        }

        $("#search_users").val(new_value);
        if (new_value) {
            location.href = "/settings/users?filter=" + new_value;
        } else {
            location.href = "/settings/users?filter=" + "All Users";
        }
    }
});


$("#btnUsers").on("click", function () {
    active_element = $(".nav-item.active.current-page").attr("id");
    $("#" + active_element).removeClass("active current-page");
    $("#Users").addClass("active current-page");
    $("#" + "dv" + active_element).addClass("hide-dv");
    $("#dvUsers").removeClass("hide-dv");
});

$("#btnDiscuss").on("click", function () {
    active_element = $(".nav-item.active.current-page").attr("id");
    $("#" + active_element).removeClass("active current-page");
    $("#Discuss").addClass("active current-page");
    $("#" + "dv" + active_element).addClass("hide-dv");
    $("#dvDiscuss").removeClass("hide-dv");
});

$("#toggle-anchr").on("click", function () {
    if ($(this).hasClass("active")) {
        $(".nk-aside").hide();
    } else {
        $(".nk-aside").show();
    }
});

$(".close").on("click", function () {
    var id = $(this).attr("id");
    var modal = $("#modal" + id);
    modal.attr("class", "modal fade");
    modal.css("display", "none");
    backdrop.attr("class", "modal-backdrop fade");
    backdrop.css("display", "none");
});

$(".install").on("click", function () {
    var module_id = $(this).attr("id");
    var module_name = $(this).attr("name");
    $("#sp_module").text(module_name);
    var modal = $("#modalInstalling");
    modal.attr("class", "modal fade show");
    modal.css("display", "block");
    backdrop.attr("class", "modal-backdrop fade show");
    backdrop.css("display", "block");
    $.post("/install_module", {
        module_id: module_id,
    })
        .done(function (response) {
            modal.attr("class", "modal fade");
            modal.css("display", "none");
            backdrop.attr("class", "modal-backdrop fade");
            backdrop.css("display", "none");
            route = response["name"].toLowerCase() + ".dashboard";

            location.href = Flask.url_for(route);
        })
        .fail(function () {
            $(destElem).text("{{ _('Error: Could not contact server.') }}");
        });
});

$("#btn_addProduct").on("click", function () {
    var modal = $("#modalAddProduct");
    modal.attr("class", "modal fade show");
    modal.css("display", "block");
    backdrop.attr("class", "modal-backdrop fade show");
    backdrop.css("display", "block");
});

$("#anchor_customer").on("click", function () {
    var active_anchr = $(".nav-link.active");
    var active_link = $(".nav-item.active.current-page");
    var closed_dv = $(".dv-none");
    var open_dv = $(".dv-block");
    active_anchr.attr("class", "nav-link");
    active_link.attr("class", "nav-item");
    $("#anchor_customer").attr("class", "nav-link active");
    open_dv.attr("class", "dv-none");
    closed_dv.attr("class", "dv-block");
    return false;
});

$("#anchor_quotation").on("click", function () {
    var active_anchr = $(".nav-link.active");
    var active_link = $(".nav-item.active.current-page");
    var closed_dv = $(".dv-none");
    var open_dv = $(".dv-block");
    active_anchr.attr("class", "nav-link");
    active_link.attr("class", "nav-item");
    $("#anchor_quotation").attr("class", "nav-link active");
    open_dv.attr("class", "dv-none");
    closed_dv.attr("class", "dv-block");
    return false;
});

$(".back").click(function (e) {
    e.preventDefault();
    $("#dv_new_database").css("display", "block");
    $("#dv_start_now").css("display", "none");
    $(".continue").css("display", "block");
    $("#responsivePricingPanel").css("display", "block");
    return false;
});

$(".close").click(function (e) {
    e.preventDefault();
    $("#modalAlert").removeClass("show");
    $("#modalAlert").hide();
    $(".modal-backdrop").hide();
});

window.onclick = function (event) {
    if ($("#modalAlert").hasClass("show")) {
        $("#modalAlert").removeClass("show");
        $("#modalAlert").hide();
        $(".modal-backdrop").hide();
    }
};

$(".confirm-delete-users").click(function (e) {
    e.preventDefault();
    $("#confirm-delete-users").modal("show");
});

$(".confirm-delete-user").click(function (e) {
    slug = $(this).attr("id");
    e.preventDefault();
    $("#confirm-delete-user").modal("show");
});

$(".confirm-archive-users").click(function (e) {
    e.preventDefault();
    $("#confirm-archive-users").modal("show");
});

$(".confirm-archive-user").click(function (e) {
    slug = $(this).attr("id");
    e.preventDefault();
    $("#confirm-archive-user").modal("show");
});

$(".delete-users").click(function (e) {
    e.preventDefault();
    $.post("/settings/delete_users", {
        selected_users: selectedUsers,
    }).done(function (response) {
        if (response["response"] == "current user") {
            alert("You cannot delete the user you're currently logged in as.");
        } else if (response["response"] == "success") {
            window.location.reload();
        }
    });
});

$(".delete-user").click(function (e) {
    e.preventDefault();
    $.post("/settings/delete_user", {
        selected_user: slug,
    }).done(function (response) {
        if (response["response"] == "current user") {
            alert("You cannot delete the user you're currently logged in as.");
        } else if (response["response"] == "success") {
            window.location.reload();
        }
    });
});

$(".archive-users").click(function (e) {
    e.preventDefault();
    $.post("/settings/archive-users", {
        selected_users: selectedUsers,
    }).done(function (response) {
        if (response["response"] == "current user") {
            alert("You cannot deactivate the user you're currently logged in as.");
        } else if (response["response"] == "success") {
            window.location.reload();
        }
    });
});

$(".archive-user").click(function (e) {
    e.preventDefault();
    $.post("/settings/archive_user", {
        selected_user: slug,
    }).done(function (response) {
        if (response["response"] == "current user") {
            alert("You cannot deactivate the user you're currently logged in as.");
        } else if (response["response"] == "success") {
            window.location.reload();
        }
    });
});

$(".unarchive-users").click(function (e) {
    e.preventDefault();
    $.post("/settings/unarchive-users", {
        selected_users: selectedUsers,
    }).done(function (response) {
        if (response["response"] == "success") {
            window.location.reload();
        }
    });
});

$(".unarchive-user").click(function (e) {
    e.preventDefault();
    slug = $(this).attr("id").split("unarchive.")[1];
    $.post("/settings/unarchive_user", {
        selected_user: slug,
    }).done(function (response) {
        if (response["response"] == "success") {
            window.location.reload();
        }
    });
});

$(".add-users").click(function (e) {
    e.preventDefault();
    slug = $(".span-new-group").attr("id");
    if (selectedUsers.length == 0) {
        alert("Select atleast 1 user");
    } else {
        $.post("/settings/select_users", {
            slug: slug,
            selected_users: selectedUsers,
        }).done(function (response) {
            window.location.reload();
        });
    }
});

$(".new-users").click(function (e) {
    e.preventDefault();
    if (selectedUsers.length == 0) {
        alert("Select atleast 1 user");
    } else {
        $.post("/settings/select_users", {
            selected_users: selectedUsers,
        }).done(function (response) {
            location.href = "/settings/new_group/" + response["slug"];
        });
    }
});

$(".select-group").click(function (e) {
    slug = $(this).attr("id");
    location.href = "/settings/group/" + slug;
});

$(".select-user").click(function (e) {
    slug = $(this).closest("tr").attr("id");
    location.href = "/settings/user/" + slug;
});

$(".remove-user").click(function (e) {
    e.preventDefault();
    slug = this.id.split(".")[0];
    user_id = this.id.split(".")[1];
    $.post("/settings/remove_user", {
        slug: slug,
        user_id: user_id,
    })
        .done(function (response) {
            window.location.reload();
        })
        .fail(function () { });
});

$(".confirm-delete-group").click(function (e) {
    e.preventDefault();
    $("#confirm-delete-group").modal("show");
});

$(".delete-group").click(function (e) {
    e.preventDefault();
    var _deletegroup = sessionStorage.getItem("_delete-group");
    if (_deletegroup) {
        sessionStorage.removeItem("_delete-group");
        $.post("/settings/delete-group", {
            selected_groups: selectedGroups,
        }).done(function (response) {
            window.location.reload();
        });
    } else {
        $.post("/settings/delete-group", {
            selected_groups: selectedGroups,
        }).done(function (response) {
            window.location.reload();
        });
    }
});

$("._delete-group").click(function (e) {
    e.preventDefault();
    selectedGroups.push($(this).attr("id"));
    sessionStorage.setItem("_delete-group", "true");
    $("#confirm-delete-group").modal("show");
});

$(".submit-access-right").click(function (e) {
    e.preventDefault();
    slug = $(".span-new-group").attr("id");
    if ($("#add_access_name").val().length == 0) {
        alert("Provide a name for this record");
    } else if ($("#select_model").val() == "default_option") {
        alert("Select a model for this record");
    } else {
        $.post("/settings/access-right", {
            access_name: access_name,
            model: selected_model,
            group: slug,
            read: read,
            write: write,
            create: create,
            delete: _delete,
        }).done(function (response) {
            if (response["response"] == "access name exists") {
                alert("An access right with this name exists.");
            } else {
                sessionStorage.setItem("reloading", "true");
                window.location.reload();
            }
        });
    }
});

$(".th_accessName").click(function () {
    id_of_access_right = $(this).closest("tr").prop("id");
    span_access_class = $(this).children("span").attr("class");
    $(this).children("span").hide();
    $(this).children("input").show();
});

$(".update_model").click(function () {
    id_of_access_right = $(this).closest("tr").prop("id");
    span_model_class = $(this).children("span").attr("class");
    $(this).children("span").hide();
    $(this).children("input").show();
});

$(".update_model").click(function () {
    id_of_access_right = $(this).closest("tr").prop("id");
    $(this).children("span").hide();
    $(this).children("div").show();
});

$(".first-opportunity").click(function (e) {
    stage_id = getId(this.id);
    e.preventDefault();

    $("#new_item-" + stage_id).show();
    pipeline_stage(stage_id);
    $("#modalAlert").removeClass("show");
    $("#modalAlert").hide();
    $(".modal-backdrop").hide();
});

// update item priority
$(".select-priority-update").click(function (e) {
    e.preventDefault();
    var el, el2, el3;
    var value;
    item_id = this.name;
    el = $("#_priority1-" + item_id);
    el2 = $("#_priority2-" + item_id);
    el3 = $("#_priority3-" + item_id);
    if (this.id === "_selectPriority1-" + item_id) {
        if (el.hasClass("asterisk-off")) {
            el.removeClass("asterisk-off");
            el.removeClass("ni-star");
            el.addClass("ni-star-fill");
            value = 1;
            update_priority(item_id, value);
        } else {
            el.removeClass("ni-star-fill");
            el.addClass("asterisk-off");
            el.addClass("ni-star");
            el2.removeClass("ni-star-fill");
            el2.addClass("asterisk-off");
            el2.addClass("ni-star");
            el3.removeClass("ni-star-fill");
            el3.addClass("asterisk-off");
            el3.addClass("ni-star");
            value = 0;
            update_priority(item_id, value);
        }
    } else if (this.id === "_selectPriority2-" + item_id) {
        if (el2.hasClass("asterisk-off")) {
            el.removeClass("asterisk-off");
            el.removeClass("ni-star");
            el.addClass("ni-star-fill");
            el2.removeClass("asterisk-off");
            el2.removeClass("ni-star");
            el2.addClass("ni-star-fill");
            value = 2;
            update_priority(item_id, value);
        } else {
            el2.removeClass("ni-star-fill");
            el2.addClass("asterisk-off");
            el2.addClass("ni-star");
            el3.removeClass("ni-star-fill");
            el3.addClass("asterisk-off");
            el3.addClass("ni-star");
            value = 1;
            update_priority(item_id, value);
        }
    } else if (this.id === "_selectPriority3-" + item_id) {
        if (el3.hasClass("asterisk-off")) {
            el.removeClass("asterisk-off");
            el.removeClass("ni-star");
            el.addClass("ni-star-fill");
            el2.removeClass("asterisk-off");
            el2.removeClass("ni-star");
            el2.addClass("ni-star-fill");
            el3.removeClass("asterisk-off");
            el3.removeClass("ni-star");
            el3.addClass("ni-star-fill");
            value = 3;
            update_priority(item_id, value);
        } else {
            el3.removeClass("ni-star-fill");
            el3.addClass("asterisk-off");
            el3.addClass("ni-star");
            value = 2;
            update_priority(item_id, value);
        }
    }
});

$(".discard-item").click(function (e) {
    e.preventDefault();
    stage_id = getId(this.id);
    $("#new_item-" + stage_id).fadeOut("slow");
});

// add new stage
$("#addBoard").click(function (e) {
    e.preventDefault();
    $("#modalAddStage").modal("show");
});

// handle edit stage submit event
$("#submit_new_stage").click(function (e) {
    e.preventDefault();
    stage_name = $("#new_stage_name").val();
    $("#stage_title_" + stage_id).html(stage_name);
    add_stage();
});

$(".filter-pipeline").click(function (e) {
    e.preventDefault();
    filter_id = $(this).attr("id");
    var filter_name = $(this).children("span").text();
    if ($(this).find('em.ni-check-thick').length > 0) {
        $(this).find('em.ni-check-thick').remove();
        if (filter_name.indexOf(selected_filters) == -1) {
            $(".lead-items .kanban-drag").fadeOut();
            $("#search_pipeline").val(function () {
                return $.trim(this.value.replace(filter_name + ",", ""));
            })
            removeParam(filter_name)
            clear_pipeline_filter(filter_name);
        } else if (filter_name.indexOf($(this).val()) == -1) {
            $(".lead-items .kanban-drag").fadeOut();
            $("#search_pipeline").val(function () {
                return $.trim(this.value.replace(filter_name + ",", ""));
            })
            
            add_pipeline_filter(filter_id);
        }
    } else {
        // append before span
        $(this).find('span').before("<em class='icon ni ni-check-thick'></em>");
        $("#search_pipeline").val(function () {
            return this.value + " " + filter_name + ", ";
        })
        updateURLParameter(window.location.href, filter_name, true)
    }
    // if (hasClass($(this).children("em"), "ni-check-thick")) {
    //     const index = selectedFilters.indexOf(filter_id);
    //     selectedFilters.splice(index, 1);
    //     $(this).children("em").removeClass("ni-check-thick");
    //     var current_value = $("#search_pipeline").val();
    //     if (current_value == "All") {
    //         new_value = current_value.replace("All" + ",", "");
    //     } else {
    //         new_value = current_value.replace(filter_name + ",", "");
    //     }
    //     $("#search_pipeline").val(new_value);
    //     if (new_value) {
    //         location.href = "/crm?filter=" + new_value;
    //     } else {
    //         location.href = "/crm?filter=" + "All";
    //     }
    // } else {
    //     selectedFilters.push(filter_id);
    //     $(this).children("em").addClass("ni-check-thick");
    //     var current_value = $("#search_pipeline").val();
    //     if (current_value == "All") {
    //         new_value = current_value.replace("All", filter_name + ", ");
    //     } else {
    //         new_value = current_value + filter_name + ", ";
    //     }
    //     $("#search_pipeline").val(new_value);
    //     if (new_value) {
    //         location.href = "/crm?filter=" + new_value;
    //     } else {
    //         location.href = "/crm?filter=" + "All";
    //     }
    // }
});

$(".remove-access-right").click(function (e) {
    id_of_access_right = $(this).attr("id");
    slug = $(".span-new-group").attr("id");
    e.preventDefault();
    $.post("/settings/remove_access_right", {
        group: slug,
        access: id_of_access_right,
    }).done(function (response) {
        sessionStorage.setItem("reloading", "true");
        window.location.reload();
    });
});

$(".edit-stage").click(function (e) {
    e.preventDefault();
    stage_id = this.id;
    $("#modalEditStage").modal("show");
});

$(".delete-lead-record").click(function (e) {
    e.preventDefault();
    $("#confirmDelete").modal("show");
    $("#confirmDelete").find(".delete-record").attr("id", this.id);
})

$(".delete-record").click(function (e) {
    e.preventDefault();
    lead_id = getId($(this).attr("id"));
    delete_lead(lead_id);
})

// document.addEventListener('click', function (event) {
//     var arr = data
//     var values = []
//     var isClickInside = null
//     var el;
//     if (current_href.toLowerCase().indexOf("purchase/new/request-for-quotation") >= 0) {
//         el = $(event.target).closest('tr')
//         if (el.hasClass('is-click-inside') || $(event.target).hasClass("is-click-inside") || $(event.target).hasClass("add-a-product") || $(event.target).hasClass('select2-selection__rendered') || $(event.target).hasClass('select2-selection__arrow')) {
//             isClickInside = true
//         }
//         if (!isClickInside) {
//             $(".clone-product-tr").each(function (i, e) {
//                 if ($(e).attr("id")) {
//                     count_tr = $("#purchase_body").find("tr").length;
//                     current_index = parseInt(count_tr) - 1
//                     var quantity_el = document.getElementsByClassName("inp_quantity")[current_index];
//                     var quantity = quantity_el.value
//                     $(quantity_el).css("display", "none");
//                     var quantity_span = document.createElement("span");
//                     quantity_span.innerHTML = quantity;
//                     td_quantity = document.getElementsByClassName("td_quantity")[current_index];
//                     $(quantity_span).appendTo($(td_quantity))
//                 } else {
//                     $(e).remove()
//                 }
//             })

//         }
//     }
//     if (current_href.toLowerCase().indexOf("inventory/new/product") >= 0) {
//         el = $(event.target)
//         if (type == "product_attributes") {
//             var val = $(".inp_attribute:last").val()
//             $.each(arr, function () {
//                 var key = Object.keys(this)[0];
//                 values.push(this[key])
//             })
//             if ($(el).attr("id") != $(".inp_attribute:last").attr("id")) {
//                 if (val) {
//                     if (values.includes(val)) {
//                         console.log("found")
//                     } else {
//                         $(".inp_attribute:last").val(values[0])
//                     }
//                 }
//             }
//         }

//         if (type = "product_attributes_values") {
//             var val = $(".inp_value:last").val()
//             $.each(arr, function () {
//                 var key = Object.keys(this)[0];
//                 values.push(this[key])
//             })
//             if ($(el).attr("id") != $(".inp_value:last").attr("id")) {
//                 if (val) {
//                     if (values.includes(val)) {
//                         console.log("found")
//                     } else {
//                         // $(".inp_value:last").val(values[0])
//                     }
//                 }
//             }
//         }

//         if (el.hasClass('is-click-inside')) {
//             isClickInside = true
//         }
//         if (!isClickInside) {
//             if (!$(".inp_attribute:last").val()) {
//                 $(".clone-attribute-tr:last").remove()
//             }
//         }
//     }
// })
