// edit CRM board
var stage_id;
var stage_name;
var item_id;
var current_href;
var selected = 0;
var selectedUsers = [];
var selectedGroups = [];
var new_access_id;
var name_of_access_right;
var id_of_access_right;
var slug;
var model_id;
var model_name;
var access_name;
var selected_model;
var read = false;
var write = false;
var create = false;
var _delete = false;
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

// post board changes to server
function edit_stage() {
  $.post("/crm/edit_stage", {
    stage_id: stage_id,
    stage_name: stage_name,
  })
    .done(function (response) {
      $("#modalEditStage").modal("hide");
    })
    .fail(function () {});
}

function delete_stage() {
  $.post("/crm/delete_stage", {
    stage_id: stage_id,
  })
    .done(function (response) {
      location.href = "/crm/";
    })
    .fail(function () {});
}

function move_stage_forward() {
  $.post("/crm/move_stage_forward", {
    stage_id: stage_id,
  }).done(function (response) {
    location.href = "/crm/";
  });
}

function move_stage_behind() {
  $.post("/crm/move_stage_behind", {
    stage_id: stage_id,
  }).done(function (response) {
    location.href = "/crm/";
  });
}

// add new board item
$(".add-item").click(function (e) {
  e.preventDefault();
  stage_id = getId(this.id);
  $("#new_item_" + stage_id).show();
  pipeline_stage(stage_id);
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

// get partner details
function get_partner_details(value) {
  $.post("/crm/get_partner_details", {
    partner_id: value,
  })
    .done(function (response) {
      $("#partner_email_" + stage_id).val(response["partner_email"]);
      $("#partner_phone_" + stage_id).val(response["partner_phone"]);
    })
    .fail(function () {
      alert("Get Partner Details Error");
    });
}

$(".first-opportunity").click(function (e) {
  stage_id = getId(this.id);
  e.preventDefault();

  $("#new_item_" + stage_id).show();
  pipeline_stage(stage_id);
  $("#modalAlert").removeClass("show");
  $("#modalAlert").hide();
  $(".modal-backdrop").hide();
});

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

// post opportunity priority
function select_priority(value) {
  $.post("/crm/selected_priority", {
    selected_priority: value,
  })
    .done(function (response) {})
    .fail(function () {});
}

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

// add new recurring plan modal
$(".recurring-plan").on("change", function () {
  stage_id = getId(this.id);
  if (this.value === "new_plan") {
    $("#modalNewPlan").modal("show");
  }
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

$(".discard-item").click(function (e) {
  e.preventDefault();
  stage_id = getId(this.id);
  $("#new_item_" + stage_id).hide();
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

var filter;
$(".filter").click(function (e) {
  e.preventDefault();
  filter_id = this.id;
  filter = $("#spn_filter-" + filter_id).text();
  var filters;
  if ($(this).hasClass("selected")) {
    $(this).removeClass("selected");
    $("#chk_" + filter_id).hide();
    if ($("#search_pipeline").val()) {
      filters = $("#search_pipeline").val();
      var _filters = filters.replace(filter + ",", "");
      $("#search_pipeline").val(_filters);
      filter_pipeline(_filters);
    }
  } else {
    $(this).addClass("selected");
    $("#chk_" + filter_id).show();
    if ($("#search_pipeline").val()) {
      filters = $("#search_pipeline").val();
      $("#search_pipeline").val();
      $("#search_pipeline").val(filters + filter + ",");
      filter_pipeline(filters + filter);
    } else {
      $("#search_pipeline").val(filter + ",");
      filter_pipeline(filter);
    }
  }
});

function filter_pipeline() {}

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

// utilities
function getCookie(c_name) {
  if (document.cookie.length > 0) {
    c_start = document.cookie.indexOf(c_name + "=");
    if (c_start != -1) {
      c_start = c_start + c_name.length + 1;
      c_end = document.cookie.indexOf(";", c_start);
      if (c_end == -1) c_end = document.cookie.length;
      return unescape(document.cookie.substring(c_start, c_end));
    }
  }
  return "";
}

function getId(str) {
  return str.split("-")[1];
}

$(document).ready(function () {
  $("#Users").addClass("active current-page");
  if ($(".dv-module").length) {
    $(".dv-module").removeAttr("href");
    $(".dv-module").css("cursor", "pointer");
  }

  $("#search_pipeline").val("My Pipeline,");
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

var backdrop = $("#dv_modal-backdrop");

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

var selectedModules = [];
var price;
$(".check").on("click", function () {
  //get checkbox id element for selected app
  var elemId = $(this).attr("id");

  //get id of selected app from checkbox id
  var moduleId = elemId.split("-")[1];

  //get name of selected app
  var appTitle = $("#title-" + moduleId).text();

  //for name with multiple words split app name into separate strings
  var splitAppTitle = appTitle.split(" ");

  if ($("#check-" + moduleId).prop("checked") == false) {
    //get index of app to remove from selection
    const index = selectedModules.indexOf(moduleId);

    //remove unselected app
    selectedModules.splice(index, 1);

    //deselect div element associated with app
    $("#dv-" + moduleId).removeClass("bordered-focus");

    //set number of selected apps
    $(".noApps").text(selectedModules.length);

    //remove unselected from list of selected apps
    $("#" + splitAppTitle[0]).remove();

    price = 600 * selectedModules.length;

    $(".total_price").text(price);
  } else {
    //insert id of selected app
    selectedModules.push(moduleId);

    //select/highlight div element assosciated with selected app
    $("#dv-" + moduleId).addClass("bordered-focus");

    //pop up for selected apps
    $(".nk-aside").css("display", "block");
    $("#responsivePricingPanel").css("display", "block");

    //set number of selected apps
    $(".noApps").text(selectedModules.length);

    //include selected app in pop up of selected apps
    $(".ul_apps").append(
      "<li id=" + splitAppTitle[0] + ">" + appTitle + "</li>"
    );

    //add price
    price = 600 * selectedModules.length;

    $(".total_price").text(price);
  }
  if (selectedModules.length === 0) {
    $(".nk-aside").css("display", "none");
    $("#responsivePricingPanel").css("display", "none");
  }
});

$(".dv-module").on("click", function () {
  var elemId = $(this).attr("id");
  var moduleId = elemId.split("-")[1];
  var appTitle = $("#title-" + moduleId).text();
  var splitAppTitle = appTitle.split(" ");

  if ($("#check-" + moduleId).prop("checked") == false) {
    selectedModules.push(moduleId);

    $("#check-" + moduleId).prop("checked", true);
    $("#dv-" + moduleId).addClass("bordered-focus");
    $(".nk-aside").css("display", "block");
    $("#responsivePricingPanel").css("display", "block");

    $(".noApps").text(selectedModules.length);
    $(".ul_apps").append(
      "<li id=" + splitAppTitle[0] + ">" + appTitle + "</li>"
    );
    //add price
    price = 600 * selectedModules.length;

    $(".total_price").text(price);
  } else {
    const index = selectedModules.indexOf(moduleId);

    selectedModules.splice(index, 1);

    $("#check-" + moduleId).prop("checked", false);
    $("#dv-" + moduleId).removeClass("bordered-focus");

    $(".noApps").text(selectedModules.length);
    $("#" + splitAppTitle[0]).remove();

    price = 600 * selectedModules.length;

    $(".total_price").text(price);
  }
  if (selectedModules.length === 0) {
    $(".nk-aside").css("display", "none");
    $("#responsivePricingPanel").css("display", "none");
  }
});

function pipeline_stage(value) {
  $.post("/crm/pipeline_stage", {
    pipeline_stage: value,
  })
    .done(function (response) {})
    .fail(function () {});
}

function edit_domain() {
  $("#dvDomainOutput").css("display", "block");
  $("input[name=domainoutput]").val(function (index, value) {
    return value.replace(".olam-erp.com", "");
  });
  $(".form-text-hint").css("display", "block");
  $("#domainoutput").attr("readonly", false);
}

$(".back").click(function (e) {
  e.preventDefault();
  $("#dv_new_database").css("display", "block");
  $("#dv_start_now").css("display", "none");
  $(".continue").css("display", "block");
  $("#responsivePricingPanel").css("display", "block");
  return false;
});

$("#company").change(function () {
  var text = $(this).val();
  $("#domain").val(text);
});

// $('.start-now').click(function (e) {
//   e.preventDefault()
//   $('#dv_start_now').css('display', 'none')
//   $('#dv_loading').css('display', 'block')
//   return false
// })

$(function () {
  $("#txtcompany").keyup(function () {
    $("#dv_domain").css("display", "block");
    $("#dvDomainOutput").css("display", "block");
    $("#sp_domain").text(
      this.value.replace(/ /g, "-").toLowerCase() + ".olam-erp.com"
    );
    $("#domainoutput").val(
      this.value.replace(/ /g, "-").toLowerCase() + ".olam-erp.com"
    );
  });
});

$(window).bind("scroll", function () {
  if ($(window).scrollTop() > 100) {
    $("#responsivePricingPanel").hide();
  } else {
    $("#responsivePricingPanel").show();
  }
});

jQuery(document).ready(function () {
  $("#frm_setup").submit(function (e) {
    e.preventDefault();
    var form = $(this);
    var url = form.attr("action");

    $(".nk-main").hide();
    $("#bdy_newdb").addClass("bg-black").removeClass("bg-white");
    $("#modalInstalling").modal({ backdrop: "static", keyboard: false });
    $("#modalInstalling").modal("show");

    $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(),
      success: function (data) {
        location.href = "/home";
      },
    });
  });
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

$("#select_country").change(function () {
  country = $(this).val();
  get_city(country);
});

current_href = $(location).attr("href");

if (current_href.toLowerCase().indexOf("contacts/view_contact") >= 0) {
  if (
    $("#select_country").val() !== "default_option" &&
    $("#select_city").val() !== "default_option"
  ) {
    console.log($("#select_country").val());
    console.log($("#select_city").val());
    country = $("#select_country").val();
    get_city(country);
  }
}

async function get_city(country) {
  const rawResponse = await fetch("/contacts/get_cities", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({ country: country }),
  });
  const content = await rawResponse.json();

  $("#select_city").find("option").remove();
  $("#select_city").append($("<option>", { value: "#", text: "Select City" }));
  $.map(content["cities"]["items"], function (value, key) {
    $("#select_city").append(
      $("<option>", { value: value["id"], text: value["name"] })
    );
  });
}

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

function updateTextView(_obj) {
  var num = getNumber(_obj.val());
  if (num == 0) {
    _obj.val("");
  } else {
    _obj.val(num.toLocaleString());
  }
}
function getNumber(_str) {
  var arr = _str.split("");
  var out = new Array();
  for (var cnt = 0; cnt < arr.length; cnt++) {
    if (isNaN(arr[cnt]) == false) {
      out.push(arr[cnt]);
    }
  }
  return Number(out.join(""));
}
$(document).ready(function () {
  $(".expected_revenue").on("keyup", function () {
    updateTextView($(this));
  });
});

function update_priority(item_id, priority) {
  $.post("/crm/update_item", {
    item_id: item_id,
    priority: priority,
  })
    .done(function (response) {})
    .fail(function () {});
}

$(".chk-user").change(function () {
  var user_id = $(this).attr("id");
  if (this.checked) {
    $(".select-user").addClass("btn-primary").removeClass("btn-secondary");
    $(".add-users").addClass("btn-primary").removeClass("btn-secondary");
    $(".new-users").addClass("btn-primary").removeClass("btn-secondary");
    selected = selected + 1;
    $(".selected").css("display", "block");
    $(".selected").text(selected + " selected");
    selectedUsers.push(user_id);
  } else {
    const index = selectedUsers.indexOf(user_id);
    selectedUsers.splice(index);

    if (selected != 0) {
      selected = selected - 1;
      $(".selected").text(selected + " selected");
    } else {
      $(".selected").css("display", "none");
    }
    if ($(".chk-user").is(":checked")) {
    } else {
      $(".select-user").addClass("btn-secondary").removeClass("btn-primary");
      $(".add-users").addClass("btn-secondary").removeClass("btn-primary");
      $(".new-users").addClass("btn-secondary").removeClass("btn-primary");
    }
  }
});

function select_users() {
  if (selectedUsers.length == 0) {
    alert("Select atleast 1 user");
  } else {
    $.post("/settings/select_users", {
      selected_users: selectedUsers,
    }).done(function (response) {
      window.location.reload();
    });
  }
}

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
          if (current_href.toLowerCase().indexOf("settings/edit_group") >= 0) {
            location.href = "/settings/group/" + slug;
          }
        }
      },
    });
  }
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

$(".select-group").click(function (e) {
  slug = $(this).attr("id");
  location.href = "/settings/group/" + slug;
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
    .fail(function () {});
});

$(".group-check").change(function (e) {
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

$(".confirm-delete-group").click(function (e) {
  e.preventDefault();
  console.log(selectedGroups);
  $("#confirm-delete-group").modal("show");
});

$(".delete-group").click(function (e) {
  e.preventDefault();
  $.post("/settings/delete-group", {
    selected_groups: selectedGroups,
  }).done(function (response) {
    window.location.reload();
  });
});

async function get_models() {
  const rawResponse = await fetch("/settings/get_models", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
  });

  const content = await rawResponse.json();
  console.log(content["items"].length);
  for (var i = 0; i < content["items"].length; i++) {
    console.log(content["items"][i]["id"], content["items"][i]["name"]);
    $("#select_" + new_access_id).append(
      $("<option>", {
        value: content["items"][i]["id"],
        text: content["items"][i]["name"],
      })
    );
  }
}

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

window.onload = function () {
  var reloading = sessionStorage.getItem("reloading");
  if (reloading) {
    sessionStorage.removeItem("reloading");
    displayAccess();
  }
};

function displayAccess() {
  $("#access_rights").addClass("active");
  $("#lnk_access_rights").addClass("active");
  $("#lnk_users").removeClass("active");
  $("#users").removeClass("active");
}

$(".td_update_name_of_access_right").click(function () {
  id_of_access_right = $(this).closest("tr").prop("id");
  $(this).children("span").hide();
  $(this).children("input").show();
});

$(".update_model").click(function () {
  id_of_access_right = $(this).closest("tr").prop("id");
  $(".sp_access_model").hide();
  $(".dv_select_model").show();
});

$(".update_access_right_name").change(function () {
  name_of_access_right = $(this).val();
  $.post("/settings/access-right", {
    name: name_of_access_right,
    access: id_of_access_right,
  }).done(function (response) {
    $(".update_access_right_name").hide();
    $(".sp_name_of_access_right").show();
    $(".sp_name_of_access_right").text(name_of_access_right);
  });
});

$(".select_model").change(function () {
  selected_model = $(this).val();
  $.post("/settings/access-right", {
    access: id_of_access_right,
    model_id: selected_model,
  }).done(function (response) {
    $(".dv_select_model").hide();
    $(".sp_access_model").show();
    $(".sp_access_model").text(response["model_name"]);
  });
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

function get_item() {
  $.ajaxSetup({
    headers: { "X-CSRFToken": getCookie("csrftoken") },
  });

  var item_id = document.getElementById("item").value;
  $.post("/dashboarditem_selling_price", {
    item_id: item_id,
  }).done(function (response) {
    document.getElementById("unit_price").value = response["unit_price"];
  });
}
