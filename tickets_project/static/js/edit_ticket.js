jQuery.validator.setDefaults({
    success: "valid"
});;

function validateForm() {
    $("#ticket").validate({
        rules: {
            type: "required",
            team: "required",
            urgence: "required",
            subscriber_type: "required",
            address: "required",
            description: "required",
            account: {digits: true}
        },
        messages: {
            type: "Выберите тип заявки.",
            team: "Выберите бригаду.",
            urgence: "Выберите срочность.",
            subscriber_type: "Выберите тип абонента.",
            address: "Введите адрес.",
            description: "Введите описание.",
            reason: "Выберите причину.",
            account: "Введите только цифры.",
            solution: "Введите решение.",
        },
    });
}

function submitTicket() {
    $('#id_solution').removeClass("required");
    $('#id_reason').removeClass("required");
    if ($("#ticket").valid()) {
        $('#ticket').submit();
    }
}

function closeTicket() {
    $('#id_solution').addClass("required");
    $('#id_reason').addClass("required");
    if ($("#ticket").valid()) {
        $('#id_status').val("False");
        $('#ticket').submit();
    }
}

$(function() {
    minutes_settings = {
        stepMinute: 30,
    };
    $('#id_date_assigned').datetimepicker(minutes_settings);
    $('<a class="additional_action" href="javascript:getSubscriberData()">Загрузить данные</a>').insertAfter($('#id_account'));
    $('<a class="additional_action" href="javascript:openMap()">Открыть карту</a>').insertAfter($('#id_address'));
    $('#id_time').timepicker(minutes_settings);
    validateForm();
});

function openMap() {
    function removeAppartment(address) {
        x = address.indexOf(', кв.');
        return address.substring(0, x);
    }
    address = $('#id_address').val();
    address = removeAppartment(address);
    window.open('https://maps.google.ru/maps?q=' + city + ', ' + address);
}

function getSubscriberData() {
    $.post("http://stat.astsystems.ru/scripts/get_subscriber_data.php", {'account': $('#id_account').val()},
        function(data) {
            data = jQuery.parseJSON(data);
            if (data.status) {
                $('#id_name').val(data.name);
                $('#id_address').val(data.address);
                $('#id_phone').val(data.phone);
                $('#id_technical_data').val(data.technical_data);
            } else {
                displayMessage('Абонент с данным номером договора отсутствует в базе');
            }
        }
    ).error(function() {
        displayMessage('Ошибка получения данных');
    });
}