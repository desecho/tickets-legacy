var clear_filters = false;
function get_ticket_list() {
  $.getJSON(url_ajax_get_ticket_list,
    function(data) {
      $('#results').html('<table cellpadding="0" cellspacing="0" border="0" class="display" id="results_table"></table>');
      $('#results_table').dataTable( {
        "aaData": data.data,
        "aoColumns": [
          { "sTitle": "Id" },
          { "sTitle": "Статус" },
          { "sTitle": "Тип<br>заявки" },
          { "sTitle": "Бригада" },
          { "sTitle": "Срочность" },
          { "sTitle": "Тип<br>абонента" },
          { "sTitle": "№ Договора" },
          { "sTitle": "Адрес" },
          { "sTitle": "Длительность" },
          { "sTitle": "Дата/Время" },
          { "sTitle": "Действие" },
        ],
        "oLanguage": {
          "sProcessing":   "Подождите...",
          "sLengthMenu":   "Показать _MENU_ записей",
          "sZeroRecords":  "Записи отсутствуют.",
          "sInfo":         "Записи с _START_ до _END_ из _TOTAL_ записей",
          "sInfoEmpty":    "Записи с 0 до 0 из 0 записей",
          "sInfoFiltered": "(отфильтровано из _MAX_ записей)",
          "sInfoPostFix":  "",
          "sSearch":       "Поиск:",
          "sUrl":          "",
          "oPaginate": {
            "sFirst":      "Первая",
            "sPrevious":   "Предыдущая",
            "sNext":       "Следующая",
            "sLast":       "Последняя"
          }
        }
      });
    }
  ).error(function() {
    displayMessage('Ошибка отображения заявок');
  });
}

function array2json(arr) {
  var parts = [];
  var is_list = (Object.prototype.toString.apply(arr) === '[object Array]');

  for(var key in arr) {
    var value = arr[key];
    if(typeof value == "object") { //Custom handling for arrays
      if(is_list) parts.push(array2json(value)); /* :RECURSION: */
      else parts[key] = array2json(value); /* :RECURSION: */
    } else {
      var str = "";
      if(!is_list) str = '"' + key + '":';

      //Custom handling for multiple data types
      if(typeof value == "number") str += value; //Numbers
      else if(value === false) str += 'false'; //The booleans
      else if(value === true) str += 'true';
      else str += '"' + value + '"'; //All other things
      // :TODO: Is there any more datatype we should be in the lookout for? (Functions?)

      parts.push(str);
    }
  }
  var json = parts.join(",");

  if(is_list) return '[' + json + ']';//Return numerical JSON
  return '{' + json + '}';//Return associative JSON
}

function applyFilter(name, value, update) {
  $.post(url_ajax_apply_filter, {'name': name, 'value': value},
    function(data) {
      if (update) {
          get_ticket_list();
      }
    }
  ).error(function() {
    displayMessage('Ошибка применения фильтра.');
  });
}

function resetFilters() {
  function removeFilterIfExists(element) {
    if ($(element).val() != '') {
        $(element).val('');
        applyFilterGeneral(element);
    }
  }
  $('.filter').each(function() {
    removeFilterIfExists(this);
  });
  clear_filters = true;
  $(document).ajaxStop(function(){
    if (clear_filters) {
      get_ticket_list();
      clear_filters = false;
    }
  });
  $("#date_from").datepicker("option", "maxDate", null);
  $("#date_to").datepicker("option", "minDate", null);
}

function applyDateRangeFilter(update) {
  update = typeof update !== 'undefined' ? update : false;
  from = $("#date_from").val();
  to = $("#date_to").val();
  from_bool = Boolean(from);
  to_bool = Boolean(to);
  if (from_bool && to_bool) {
    applyFilter('date_range', array2json({'from': from, 'to': to}), update);
  }
  if (!from_bool && !to_bool) {
    applyFilter('date_range', '', update);
  }
}

function applyFilterGeneral(element, update) {
  update = typeof update !== 'undefined' ? update : false;
  date_range_filters = ["date_from", "date_to"];
  if ($.inArray($(element).attr('id'), date_range_filters) == -1){
    applyFilter($(element).attr('name'), $(element).val(), update);
  } else {
    applyDateRangeFilter(update);
  }
}

function createReport() {
  team_id = $('#team').val();
  if (team_id) {
    window.open(url_create_report + team_id);
  } else {
    displayMessage('Выберите бригаду');
  }
}

$(function() {
  $(document).ajaxStart(function(){
    $("#results").html('<div class="loading"></div>');
  });
  get_ticket_list();
  $('#date').datepicker();
  $("#date_from").datepicker({
    onSelect: function( selectedDate ) {
      $("#date_to").datepicker("option", "minDate", selectedDate);
      applyDateRangeFilter(true);
    }
  });
  $("#date_to").datepicker({
    onSelect: function( selectedDate ) {
      $("#date_from").datepicker("option", "maxDate", selectedDate);
      applyDateRangeFilter(true);
    }
  });
  $('.filter').each(function() {
    $(this).change(function(){
      applyFilterGeneral(this, true);
     });
  });
});