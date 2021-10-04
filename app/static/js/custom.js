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

$(document).ready(function () {
  $('#Users').addClass('active current-page')
  if ($('.dv-module').length) {
    $('.dv-module').removeAttr('href')
    $('.dv-module').css('cursor', 'pointer')
  }
})

$('#btnUsers').on('click', function () {
  active_element = $('.nav-item.active.current-page').attr('id')
  $('#' + active_element).removeClass('active current-page')
  $('#Users').addClass('active current-page')
  $('#' + 'dv' + active_element).addClass('hide-dv')
  $('#dvUsers').removeClass('hide-dv')
})

$('#btnDiscuss').on('click', function () {
  active_element = $('.nav-item.active.current-page').attr('id')
  $('#' + active_element).removeClass('active current-page')
  $('#Discuss').addClass('active current-page')
  $('#' + 'dv' + active_element).addClass('hide-dv')
  $('#dvDiscuss').removeClass('hide-dv')
})

$('#toggle-anchr').on('click', function () {
  if (($(this)).hasClass('active')) {
    $('.nk-aside').hide();
  } else {
    $('.nk-aside').show();
  }

})

var backdrop = $('#dv_modal-backdrop')

$('.close').on('click', function () {
  var id = $(this).attr('id')
  var modal = $('#modal' + id)
  modal.attr('class', 'modal fade')
  modal.css('display', 'none')
  backdrop.attr('class', 'modal-backdrop fade')
  backdrop.css('display', 'none')
})

$('.install').on('click', function () {
  var module_id = $(this).attr('id')
  var module_name = $(this).attr('name');
  $('#sp_module').text(module_name)
  var modal = $('#modalInstalling')
  modal.attr('class', 'modal fade show')
  modal.css('display', 'block')
  backdrop.attr('class', 'modal-backdrop fade show')
  backdrop.css('display', 'block')
  $.post('/install_module', {
    module_id: module_id
  }).done(function (response) {
    modal.attr('class', 'modal fade')
    modal.css('display', 'none')
    backdrop.attr('class', 'modal-backdrop fade')
    backdrop.css('display', 'none')
    route = response['name'].toLowerCase() + '.dashboard'
    console.log(Flask.url_for(route))
    location.href = Flask.url_for(route)
  }).fail(function () {
    $(destElem).text("{{ _('Error: Could not contact server.') }}");
  });

})

$('#btn_addProduct').on('click', function () {
  var modal = $('#modalAddProduct')
  modal.attr('class', 'modal fade show')
  modal.css('display', 'block')
  backdrop.attr('class', 'modal-backdrop fade show')
  backdrop.css('display', 'block')
})

$('#anchor_customer').on('click', function () {
  var active_anchr = $('.nav-link.active')
  var active_link = $('.nav-item.active.current-page')
  var closed_dv = $('.dv-none')
  var open_dv = $('.dv-block')
  active_anchr.attr('class', 'nav-link')
  active_link.attr('class', 'nav-item')
  $('#anchor_customer').attr('class', 'nav-link active')
  open_dv.attr('class', 'dv-none')
  closed_dv.attr('class', 'dv-block')
  return false
})

$('#anchor_quotation').on('click', function () {
  var active_anchr = $('.nav-link.active')
  var active_link = $('.nav-item.active.current-page')
  var closed_dv = $('.dv-none')
  var open_dv = $('.dv-block')
  active_anchr.attr('class', 'nav-link')
  active_link.attr('class', 'nav-item')
  $('#anchor_quotation').attr('class', 'nav-link active')
  open_dv.attr('class', 'dv-none')
  closed_dv.attr('class', 'dv-block')
  return false
})

var selectedModules = []
var price
$('.check').on('click', function () {
  //get checkbox id element for selected app
  var elemId = $(this).attr('id')

  //get id of selected app from checkbox id
  var moduleId = elemId.split('-')[1]

  //get name of selected app
  var appTitle = $('#title-' + moduleId).text()

  //for name with multiple words split app name into separate strings
  var splitAppTitle = appTitle.split(' ')

  if ($('#check-' + moduleId).prop('checked') == false) {
    //get index of app to remove from selection
    const index = selectedModules.indexOf(moduleId)

    //remove unselected app
    selectedModules.splice(index, 1)

    //deselect div element associated with app
    $('#dv-' + moduleId).removeClass('bordered-focus')

    //set number of selected apps
    $('.noApps').text(selectedModules.length)

    //remove unselected from list of selected apps
    $('#' + splitAppTitle[0]).remove()

    price = 600 * selectedModules.length

    $('.total_price').text(price)
  } else {
    //insert id of selected app
    selectedModules.push(moduleId)

    //select/highlight div element assosciated with selected app
    $('#dv-' + moduleId).addClass('bordered-focus')

    //pop up for selected apps
    $('.nk-aside').css('display', 'block')
    $('#responsivePricingPanel').css('display', 'block')

    //set number of selected apps
    $('.noApps').text(selectedModules.length)

    //include selected app in pop up of selected apps
    $('.ul_apps').append(
      '<li id=' + splitAppTitle[0] + '>' + appTitle + '</li>'
    )

    //add price
    price = 600 * selectedModules.length

    $('.total_price').text(price)
  }
  if (selectedModules.length === 0) {
    $('.nk-aside').css('display', 'none')
    $('#responsivePricingPanel').css('display', 'none')
  }
})

$('.dv-module').on('click', function () {
  var elemId = $(this).attr('id')
  var moduleId = elemId.split('-')[1]
  var appTitle = $('#title-' + moduleId).text()
  var splitAppTitle = appTitle.split(' ')

  if ($('#check-' + moduleId).prop('checked') == false) {
    selectedModules.push(moduleId)

    $('#check-' + moduleId).prop('checked', true)
    $('#dv-' + moduleId).addClass('bordered-focus')
    $('.nk-aside').css('display', 'block')
    $('#responsivePricingPanel').css('display', 'block')

    $('.noApps').text(selectedModules.length)
    $('.ul_apps').append(
      '<li id=' + splitAppTitle[0] + '>' + appTitle + '</li>'
    )
    //add price
    price = 600 * selectedModules.length

    $('.total_price').text(price)
  } else {
    const index = selectedModules.indexOf(moduleId)
    console.log(index)
    selectedModules.splice(index, 1)

    $('#check-' + moduleId).prop('checked', false)
    $('#dv-' + moduleId).removeClass('bordered-focus')

    $('.noApps').text(selectedModules.length)
    $('#' + splitAppTitle[0]).remove()
    console.log($('#' + splitAppTitle[0]).remove())

    price = 600 * selectedModules.length

    $('.total_price').text(price)
  }
  if (selectedModules.length === 0) {
    $('.nk-aside').css('display', 'none')
    $('#responsivePricingPanel').css('display', 'none')
  }
})


function select_priority(value) {
  $.post('/selected_priority', {
    selected_priority: value
  }).done(function (response) {

  }).fail(function () {

  });
}

function edit_domain() {
  $('#dvDomainOutput').css('display', 'block');
  $('input[name=domainoutput]').val(function (index, value) {
    return value.replace('.olam-erp.com', '');
  });
  $('.form-text-hint').css('display', 'block')
  $('#domainoutput').attr("readonly", false);
}


$('.back').click(function (e) {
  e.preventDefault()
  $('#dv_new_database').css('display', 'block')
  $('#dv_start_now').css('display', 'none')
  $('.continue').css('display', 'block')
  $('#responsivePricingPanel').css('display', 'block')
  return false
})

$('#company').change(function () {
  var text = $(this).val()
  $('#domain').val(text)
})

// $('.start-now').click(function (e) {
//   e.preventDefault()
//   $('#dv_start_now').css('display', 'none')
//   $('#dv_loading').css('display', 'block')
//   return false
// })

$(function () {
  $('#txtcompany').keyup(function () {
    $('#dv_domain').css('display', 'block');
    $('#dvDomainOutput').css('display', 'block');
    $('#sp_domain').text(this.value.replace(/ /g, "-").toLowerCase() + '.olam-erp.com');
    $('#domainoutput').val(this.value.replace(/ /g, "-").toLowerCase() + '.olam-erp.com');
  });
});


$(window).bind('scroll', function () {
  if ($(window).scrollTop() > 100) {
    $('#responsivePricingPanel').hide();
  }
  else {
    $('#responsivePricingPanel').show();
  }
});

jQuery(document).ready(function () {
  $('#frm_setup').submit(function (e) {
    e.preventDefault();
    var form = $(this)
    var url = form.attr('action')

    $('.nk-main').hide();
    $('#bdy_newdb').addClass('bg-black').removeClass('bg-white');
    $('#modalInstalling').modal({ backdrop: 'static', keyboard: false })
    $('#modalInstalling').modal('show');

    $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(),
      success: function (data) {
        location.href = '/home';
      }
    })
  })
})

$("#individual").change(function () {
  if (this.checked) {
    $('#company-block').hide();
    $('#individual-block').show();
  }
});

$("#company").change(function () {
  if (this.checked) {
    $('#individual-block').hide();
    $('#company-block').show();
  }
});

$('#select_country').change(function () {
  country = $(this).val();
  get_city(country);
})

async function get_city(country) {
  const rawResponse = await fetch('/contacts/get_cities', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      "X-CSRFToken": getCookie("csrftoken")
    },
    body: JSON.stringify({ country: country })
  })
  const content = await rawResponse.json();
  console.log(content['cities']['items'])
  $('#select_city').find('option').remove();
  $('#select_city').append($('<option>', { value: "#", text: "Select City" }))
  $.map(content['cities']['items'], function (value, key) {
    $('#select_city').append($('<option>', { value: value['id'], text: value['name'] }))
  })
}

$("#new_addItem").click(function (e) {
  e.preventDefault()
  $('#newItem').show();
});

$('#pipeline_select_org').on('change', function () {
  if (this.value === "add_new") {
    $('#profile-edit').modal('show');

  }
});


$('#selectPriority1').click(function (e) {
  e.preventDefault()
  var el = $('#priority1')
  var value;
  if (el.hasClass('asterisk-off')) {
    el.removeClass('asterisk-off')
    el.removeClass('ni-star')
    el.addClass('ni-star-fill');
    value = 1;
  } else {
    el.removeClass('ni-star-fill')
    el.addClass('asterisk-off')
    el.addClass('ni-star')
    value = 0;
  }
  console.log(value);

  select_priority(value);
})