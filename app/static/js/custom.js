// edit CRM board
var stage_id; // current stage for CRM
var partner_slug; // slug for current partner
var partner_id // id for current partner
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
var purchase_id;
var product_no;
var type;
var attribute;
var selected_key;
var selected_value;
var matching = {};
var matched;
var attributes = [];
var attribute_values;
var span_access_class;
var span_model_class;


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
    var price = parseInt(
      removeComma(document.getElementsByClassName("price")[1].value)
    );
    var tax_amount = (price * parseInt(tax)) / 100;
    var total_price = price + tax_amount;
    document.getElementsByClassName("total_price")[0].innerHTML =
      "(= " + insertCommas(total_price.toFixed(2)) + " INCL. TAXES)";
  });
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
  if (sessionStorage.getItem("purchase_id")) {
    purchase_id = sessionStorage.getItem("purchase_id");
  } else {
    purchase_id = null;
  }
  $.post("/purchase/new/request-for-quotation", {
    purchase_id: purchase_id,
    product_id: product_id,
  }).done(function (response) { });
}

const tags = [];
function add_tag(key, value) {
  var tag_span = document.createElement("span");
  tag_span.innerHTML = value;
  tag_span.className = "badge badge-pill badge-primary mr-1";
  $(".tags").after(tag_span);
}

function filter_pipeline() { }

function hasClass(element, cls) {
  return (" " + element.attr("class") + " ").indexOf(" " + cls + " ") > -1;
}


function renderUsers(users) {
  if (users.length > 10) {
    slicedList = user.slice(0, 20);
    for (var i = 0; i < slicedList.length; i++) { }
  } else {
    for (var i = 0; i < users["items"].length; i++) { }
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

  if (
    current_href.toLowerCase().indexOf("inventory/new/product") >= 0 ||
    current_href.toLowerCase().indexOf("/inventory/product/edit/") >= 0
  ) {
    get_attribute_values();

    document
      .getElementById("product_image")
      .addEventListener("change", readImage, false);

    $(".preview-images").sortable();

    $(".preview-images-zone").sortable();

    $(document).on("click", ".image-cancel", function () {
      let no = $(this).data("no");
      const file = $("#pro-img-" + no).attr("src");

      $(".preview-image.preview-show-" + no).remove();
      const dt = new DataTransfer();
      const input = document.getElementById("product_image");

      const { files } = input;

      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (index !== i) dt.items.add(file);
      }
      input.files = dt.files;
    });

    var num = 0;
    function readImage() {
      if (window.File && window.FileList && window.FileReader) {
        var files = event.target.files; //FileList object
        var output = $(".preview-images-zone");

        for (let i = 0; i < files.length; i++) {
          var file = files[i];

          if (!file.type.match("image")) continue;

          var picReader = new FileReader();

          picReader.addEventListener("load", function (event) {
            var picFile = event.target;
            var html =
              '<div class="col-lg-3 preview-image preview-show-' +
              num +
              '" style="padding-bottom: 14px;">' +
              '<div class="card card-bordered"><img class="card-img-top" id=pro-img-' +
              num +
              '" src="' +
              picFile.result +
              '" alt=""></div>' +
              '<div class="image-cancel" data-no="' +
              num +
              '"><em style="color: red" class="icon ni ni-trash-alt"></em></div>' +
              "</div>";
            output.append(html);
            num = num + 1;
          });
          picReader.readAsDataURL(file);
        }
      } else {
        console.log("Browser not support");
      }
    }
  }
});

var backdrop = $("#dv_modal-backdrop");

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
  var price = $(this).val();
  include_tax(price);
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


function insertAfter(referenceNode, newNode) {
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

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
  exists = [];
  if (inp && inp.classList.contains("product-name")) {
    $.each(arr, function () {
      var key = Object.keys(this)[0];
      var value = this[key];

      if (exists.indexOf(value) > -1) {
        delete this[key];
      }
      exists.push(value);
    });
  }

  /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  document.addEventListener("click", function (e) {
    if (e.target == inp) {
      var _a, _b;

      /* close any already open lists of autocompleted values */
      closeAllLists();

      /* create a DIV element that will contain the items (values): */
      _a = document.createElement("DIV");
      _a.setAttribute("class", "autocomplete-items");
      _a.setAttribute("id", e.target.id + "autocomplete-list");

      /* append the DIV element as a child of the autocomplete container: */
      e.target.parentNode.appendChild(_a);

      /* for each item in the array... */
      values = [];

      $.each(arr, function () {
        var key = Object.keys(this)[0];
        values.push(this[key]);
      });

      $.each(arr, function () {
        var key = Object.keys(this)[0];
        var value = this[key];
        _b = document.createElement("DIV");
        _b.classList.add("autocomplete-item");
        _b.classList.add("is-click-inside");
        _b.innerHTML += value;
        _b.innerHTML += "<input type='hidden' value='" + value + "'>";
        _b.getElementsByTagName("input")[0].classList.add("is-click-inside");
        _b.addEventListener("click", function (e) {
          /* insert the value for the autocomplete text field: */
          inp.value = this.getElementsByTagName("input")[0].value;
          handleChange(inp, key);
          /* close the list of autocompleted values,
              (or any other open lists of autocompleted values: */
          closeAllLists();
        });
        _a.appendChild(_b);

        // add class to input
        inp.classList.add("is-click-inside");
      });
    }
  });

  document.addEventListener("input", function (e) {
    if (e.target == inp) {
      var a,
        b,
        val = e.target.value;
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
      values = [];

      $.each(arr, function () {
        var key = Object.keys(this)[0];
        values.push(this[key]);
      });

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
          b.innerHTML =
            "<strong class='autocomplete-item'>" +
            value.substr(0, val.length) +
            "</strong>";
          b.innerHTML += value.substr(val.length);

          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + value + "'>";
          b.getElementsByTagName("input")[0].classList.add("is-click-inside");
          /*execute a function when someone clicks on the item value (DIV element):*/
          b.addEventListener("click", function (e) {
            matched = true;
            count_tr = $(".tbody").find("tr").length;
            current_index = parseInt(count_tr) - 1;

            selected_key = key;
            /*insert the value for the autocomplete text field:*/

            $(inp).val(this.getElementsByTagName("input")[0].value);

            handleChange(inp, key);
            /*close the list of autocompleted values,
                  (or any other open lists of autocompleted values:*/
            closeAllLists();
          });

          a.appendChild(b);
        }
      });

      if (!values.includes(val)) {
        b = document.createElement("DIV");
        b.classList.add("create-new-item");
        b.classList.add("is-click-inside");
        /*make the matching letters bold:*/
        b.innerHTML =
          "Create <strong class='create-new-item'>" + val + "</strong>";
        a.appendChild(b);
        b.innerHTML += "<input type='hidden' value='" + val + "'>";
        b.getElementsByTagName("input")[0].classList.add("is-click-inside");
        /*execute a function when someone clicks on the item value (DIV element):*/
        b.addEventListener("click", function (e) {
          count_tr = $(".tbody").find("tr").length;
          current_index = parseInt(count_tr) - 1;
          /*insert the value for the autocomplete text field:*/

          inp.value = this.getElementsByTagName("input")[0].value;
          handleChange(inp);

          if (inp.classList.contains("inp_value")) {
            post_product_attribute_value(inp.id.replace("inp-", ""), inp.value);
          }

          if (inp.classList.contains("inp_partner")) {
            create_partner(inp.value);
          }

          if (inp.classList.contains("inp_plan")) {
            create_plan(inp.value);
          }

          if (
            current_href.indexOf("/purchase/new/request-for-quotation") >= 0
          ) {
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
  });

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
}

function closeAllLists() {
  /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
  selected_key = "";
  var x = document.getElementsByClassName("autocomplete-items");
  for (var i = 0; i < x.length; i++) {
    x[i].parentNode.removeChild(x[i]);
  }
}

function updateURLParameter(url, param, paramVal) {
  var TheAnchor = null;
  var newAdditionalURL = "";
  var tempArray = url.split("?");
  var baseURL = tempArray[0];
  var additionalURL = tempArray[1];
  var temp = "";

  if (additionalURL) {
    var tmpAnchor = additionalURL.split("#");
    var TheParams = tmpAnchor[0];
    TheAnchor = tmpAnchor[1];
    if (TheAnchor) additionalURL = TheParams;

    tempArray = additionalURL.split("&");

    for (var i = 0; i < tempArray.length; i++) {
      if (tempArray[i].split("=")[0] != param) {
        newAdditionalURL += temp + tempArray[i];
        temp = "&";
      }
    }
  } else {
    var tmpAnchor = baseURL.split("#");
    var TheParams = tmpAnchor[0];
    TheAnchor = tmpAnchor[1];

    if (TheParams) baseURL = TheParams;
  }

  if (TheAnchor) paramVal += "#" + TheAnchor;

  var rows_txt = temp + "" + param + "=" + paramVal;
  updated_url = baseURL + "?" + newAdditionalURL + rows_txt;
  if (typeof history.pushState != "undefined") {
    var obj = { Title: "Olam", Url: updated_url };
    history.pushState(obj, obj.Title, obj.Url);
  }
}

// remove parameter
function removeParam(key) {
  sourceURL = window.location.href;

  var rtn = sourceURL.split("?")[0],
    param,
    params_arr = [],
    queryString = sourceURL.indexOf("?") !== -1 ? sourceURL.split("?")[1] : "";
  if (queryString !== "") {
    params_arr = queryString.split("&");
    for (var i = params_arr.length - 1; i >= 0; i -= 1) {
      param = params_arr[i].split("=")[0];
      if (param === key) {
        params_arr.splice(i, 1);
      }
    }
    if (params_arr.length) rtn = rtn + "?" + params_arr.join("&");
  }
  window.history.pushState("", document.title, rtn);

  return rtn;
}

