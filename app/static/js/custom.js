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
var filter;
var selectedFilters = [];
var product_desc;
var data;
var purchase_id
var product_no
var type;
var attribute;
var selected_key;
var selected_value;
var matching = {};
var matched;
var attributes = [];
var attribute_values;

function insertCommas(number) {
  if (number !== null || number !== undefined) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  } else {
    return "0.00";
  }
}

function removeComma(number) {
  return number.toString().replace(/\,/g, "");
}

function extractID(string) {
  return string.replace(/\-/g, "");
}

function include_tax(price) {
  $.get("/get_tax", function (tax) {
    var price = parseInt(removeComma(document.getElementsByClassName("price")[1].value))
    var tax_amount = (price * parseInt(tax)) / 100;
    var total_price = price + tax_amount;
    document.getElementsByClassName("total_price")[0].innerHTML = "(= " + insertCommas(total_price.toFixed(2)) + " INCL. TAXES)";
  })
}

current_href = $(location).attr("href");

if (current_href.toLowerCase().indexOf("contacts/view_contact") >= 0) {
  if (
    $(".select_country").val() !== "default_option" &&
    $(".select_city").val() !== "default_option"
  ) {
    get_city(country);
  }
}

if (current_href.toLowerCase().indexOf("settings/users") >= 0) {
  var filters = document.getElementsByClassName("filter-users");
  for (var i = 0, n = filters.length; i < n; i++) {
    child = filters[i].children[0];
    if ($(child).hasClass("ni-check-thick") == true) {
      selectedFilters.push(filters[i].id);
    }
  }
}


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

// post board changes to server
function edit_stage() {
  $.post("/crm/edit_stage", {
    stage_id: stage_id,
    stage_name: stage_name,
  })
    .done(function (response) {
      $("#modalEditStage").modal("hide");
    })
    .fail(function () { });
}

function delete_stage() {
  $.post("/crm/delete_stage", {
    stage_id: stage_id,
  })
    .done(function (response) {
      location.href = "/crm/";
    })
    .fail(function () { });
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

function post_product_purchase(product_id) {
  if (sessionStorage.getItem('purchase_id')) {
    purchase_id = sessionStorage.getItem('purchase_id');
  } else {
    purchase_id = null;
  }
  $.post("/purchase/new/request-for-quotation", {
    purchase_id: purchase_id,
    product_id: product_id
  }).done(function (response) {

  })
}



// add new board item
$(".add-item").click(function (e) {
  e.preventDefault();
  stage_id = getId(this.id);
  $("#new_item_" + stage_id).show();
  pipeline_stage(stage_id);
});


const tags = []
function add_tag(key, value) {
  var tag_span = document.createElement("span");
  tag_span.innerHTML = value;
  tag_span.className = "badge badge-pill badge-primary mr-1";
  $(".tags").after(tag_span);
}





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

function get_attribute_values() {
  $.get("/get_attribute_values", function (data) {
    attribute_values = data

    for (var i = 0; i < data.length; i++) {
      attributes.indexOf(data[i]["attribute_id"]) == -1 ? attributes.push(data[i]["attribute_id"]) : null;
    }

    for (var i = 0; i < attributes.length; i++) {

      var result = data.filter(obj => {
        return obj.attribute == attributes[i]
      })

      autocomplete(document.getElementById("inp-" + attributes[i]), result)
    }
  });
}


// get product description
function get_product_purchase_details(product) {
  $.post("/get_product_purchase_details", {
    product: product,
  }).done(function (response) {
    if (current_href.toLowerCase().indexOf("purchase/new/request-for-quotation") >= 0) {
      count_tr = $("#purchase_body").find("tr").length;
      current_index = parseInt(count_tr) - 1
      document.getElementsByClassName("inp_products")[current_index].id = "product-" + response["id"]
      $("#product-" + response["id"]).css("display", "none");
      // $(".clone-product-tr").attr("id", response["id"] + "-product-tr");
      var product_span = document.createElement("span");
      product_span.innerHTML = response['name']
      $(product_span).attr("id", "product-span-" + response['id']);
      document.getElementsByClassName("inp_quantity")[current_index].id = "quantity-for-" + response["id"]
      document.getElementsByClassName("inp_product_desc")[current_index].id = "inp-desc-for-" + response["id"]
      document.getElementsByClassName("product_description")[current_index].id = "desc-for-" + response["id"]
      document.getElementsByClassName("inp_uom")[current_index].id = "uom-for-" + response["id"]
      document.getElementsByClassName("inp_unit_price")[current_index].id = "unit-price-for-" + response['id']
      document.getElementsByClassName("sub_total")[current_index].id = "sub-total-for-" + response['id']
      $("#inp-desc-for-" + response["id"]).val(response['description']);
      $("#unit-price-for-" + response["id"]).val(response['unit_price']);
      $("#quantity-for-" + response["id"]).val("1.00");
      document.getElementById("sub-total-for-" + response['id']).innerHTML = insertCommas(response['unit_price'])

      current_total = document.getElementsByClassName("total")[0].innerHTML
      new_total = parseInt(removeComma(current_total)) + parseInt(removeComma(response['unit_price']))
      document.getElementsByClassName("total")[0].innerHTML = insertCommas(new_total)
      // $("#desc-for-" + response["id"]).text(response['description']);
      td_product = document.getElementsByClassName("td_product")[current_index];
      $(product_span).appendTo($(td_product))
      $(td_product).removeClass("w-25");
      $.get("/get_UOM", function (data) {
        autocomplete(document.getElementsByClassName("inp_uom")[current_index], data)
        return data;
      });
    }
  }).fail(function () {

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
    .done(function (response) { })
    .fail(function () { });
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

$(".filter-pipeline").click(function (e) {
  e.preventDefault();
  filter_id = $(this).attr("id");
  var filter_name = $(this).children("span").text();
  if (hasClass($(this).children("em"), "ni-check-thick")) {
    const index = selectedFilters.indexOf(filter_id);
    selectedFilters.splice(index, 1);
    $(this).children("em").removeClass("ni-check-thick");
    var current_value = $("#search_pipeline").val();
    if (current_value == "All") {
      new_value = current_value.replace("All" + ",", "");
    } else {
      new_value = current_value.replace(filter_name + ",", "");
    }
    $("#search_pipeline").val(new_value);
    if (new_value) {
      location.href = "/crm?filter=" + new_value;
    } else {
      location.href = "/crm?filter=" + "All";
    }
  } else {
    selectedFilters.push(filter_id);
    $(this).children("em").addClass("ni-check-thick");
    var current_value = $("#search_pipeline").val();
    if (current_value == "All") {
      new_value = current_value.replace("All", filter_name + ", ");
    } else {
      new_value = current_value + filter_name + ", ";
    }
    $("#search_pipeline").val(new_value);
    if (new_value) {
      location.href = "/crm?filter=" + new_value;
    } else {
      location.href = "/crm?filter=" + "All";
    }
  }
});

function filter_pipeline() { }

function hasClass(element, cls) {
  return (" " + element.attr("class") + " ").indexOf(" " + cls + " ") > -1;
}

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

function renderUsers(users) {
  if (users.length > 10) {
    slicedList = user.slice(0, 20);
    for (var i = 0; i < slicedList.length; i++) { }
  } else {

    for (var i = 0; i < users["items"].length; i++) {

    }
  }
}

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

  if (current_href.toLowerCase().indexOf("inventory/new/product") >= 0) {
    get_attribute_values()

    document.getElementById('pro-image').addEventListener('change', readImage, false);

    $(".preview-images").sortable()

    $(".preview-images-zone").sortable();

    $(document).on('click', '.image-cancel', function () {
      let no = $(this).data('no');
      $(".preview-image.preview-show-" + no).remove();
    });

    var num = 1;
    function readImage() {
      if (window.File && window.FileList && window.FileReader) {
        var files = event.target.files; //FileList object
        var output = $(".preview-images-zone");

        for (let i = 0; i < files.length; i++) {
          var file = files[i];
          if (!file.type.match('image')) continue;

          var picReader = new FileReader();

          picReader.addEventListener('load', function (event) {
            var picFile = event.target;
            var html = '<div class="preview-image preview-show-' + num + '">' +
              '<div class="image-cancel" data-no="' + num + '">x</div>' +
              '<div class="image-zone"><img id="pro-img-' + num + '" src="' + picFile.result + '"></div>' +
              '</div>';

            output.append(html);
            num = num + 1;
          });

          picReader.readAsDataURL(file);
        }
        $("#pro-image").val('');
      } else {
        console.log('Browser not support');
      }
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
    .done(function (response) { })
    .fail(function () { });
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

  $(".select_city").find("option").remove();
  $(".select_city").append($("<option>", { value: "#", text: "Select City" }));
  $.map(content["cities"]["items"], function (value, key) {
    $(".select_city").append(
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
    .done(function (response) { })
    .fail(function () { });
}


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

  for (var i = 0; i < content["items"].length; i++) {

    $("#select_" + new_access_id).append(
      $("<option>", {
        value: content["items"][i]["id"],
        text: content["items"][i]["name"],
      })
    );
  }
}



$(".price").on("keyup", function () {
  var price = $(this).val()
  include_tax(price)
})

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

var span_access_class;
$(".th_accessName").click(function () {
  id_of_access_right = $(this).closest("tr").prop("id");
  span_access_class = $(this).children("span").attr("class");
  $(this).children("span").hide();
  $(this).children("input").show();
});

var span_model_class;
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

function insertAfter(referenceNode, newNode) {
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}



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

function autocomplete(inp, arr) {

  /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  document.addEventListener("input", function (e) {
    if (e.target == inp) {
      var a, b, val = e.target.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) {
        return false;
      }
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", e.target.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      e.target.parentNode.appendChild(a);
      /*for each item in the array...*/
      values = []

      $.each(arr, function () {
        var key = Object.keys(this)[0];
        values.push(this[key])
      })
      $.each(arr, function () {
        var key = Object.keys(this)[0];
        var value = this[key];
        /*check if the item starts with the same letters as the text field value:*/
        if (value && value.toLowerCase().includes(val.toLowerCase())) {
          /*create a DIV element for each matching element:*/
          matching[key] = value;
          b = document.createElement("DIV");
          b.classList.add("is-click-inside");
          b.classList.add("autocomplete-item");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong class='autocomplete-item'>" + value.substr(0, val.length) + "</strong>";
          b.innerHTML += value.substr(val.length);

          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + value + "'>";
          b.getElementsByTagName("input")[0].classList.add("is-click-inside");
          /*execute a function when someone clicks on the item value (DIV element):*/
          b.addEventListener("click", function (e) {
            matched = true
            count_tr = $(".tbody").find("tr").length;
            current_index = parseInt(count_tr) - 1
            selected_key = key;
            /*insert the value for the autocomplete text field:*/
            $(inp).val(this.getElementsByTagName("input")[0].value);
            $("#hidden-" + inp.id).val(key)

            handleChange(inp)
            /*close the list of autocompleted values,
                  (or any other open lists of autocompleted values:*/
            closeAllLists();
          });

          a.appendChild(b);
        }
      })


      if (!values.includes(val)) {
        b = document.createElement("DIV");
        b.classList.add("create-new-item");
        b.classList.add("is-click-inside");
        /*make the matching letters bold:*/
        b.innerHTML = "Create <strong class='create-new-item'>" + val + "</strong>";
        a.appendChild(b);
        b.innerHTML += "<input type='hidden' value='" + val + "'>";
        b.getElementsByTagName("input")[0].classList.add("is-click-inside");
        /*execute a function when someone clicks on the item value (DIV element):*/
        b.addEventListener("click", function (e) {
          count_tr = $(".tbody").find("tr").length;
          current_index = parseInt(count_tr) - 1
          /*insert the value for the autocomplete text field:*/

          inp.value = this.getElementsByTagName("input")[0].value;
          handleChange(inp)

          if (current_href.indexOf("/inventory/new/product") >= 0) {
            if (inp.classList.contains("inp_value")) {
              post_product_attribute_value((inp.id).replace("inp-", ""), inp.value);
            }
          }

          if (current_href.indexOf("/purchase/new/request-for-quotation") >= 0) {
            if (inp.classList.contains("inp_products")) {
              $("#AddProductModal").modal("show");
            }
            if (inp.classList.contains("inp_vendor")) {
              $("#AddPartner").modal("show");
            }
          }

          /*close the list of autocompleted values,
                (or any other open lists of autocompleted values:*/
          closeAllLists();
        });
      }
    }
  })

  /*execute a function presses a key on the keyboard:*/
  document.addEventListener("keydown", function (e) {
    if (e.target == inp) {
      var x = document.getElementById(e.target.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
            increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) {
        //up
        /*If the arrow UP key is pressed,
            decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
    }
  });

  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = x.length - 1;
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
      except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
    closeAllLists(e.target);
  });
}

