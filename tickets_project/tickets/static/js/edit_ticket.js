jQuery.validator.setDefaults({
    success: 'valid'
});

jQuery.validator.addMethod('no_connection', function(value, element) {
    var team_id = parseInt(value);
    if (no_connection_team_ids.indexOf(team_id) !== -1) {
        return parseInt($('#id_type').val()) !== 1;
    }
    return true;
});

jQuery.validator.addMethod('no_phone', function(value, element) {
	if (parseInt($('#id_type').val()) == 1) {
		return value;
	}
    return true;
});

function validateForm() {
    $('#ticket').validate({
        rules: {
            type: 'required',
            subscriber_type: 'required',
            urgence: 'required',
            name: 'required',
            team: {
                required: true,
                no_connection: true,
            },
            phone: {
            	digits: true,
            	no_phone: true},
            address: 'required',
            description: 'required',
            account: {digits: true}
        },
        messages: {
            type: 'Выберите тип заявки.',
            name: 'Введите ФИО.',
            subscriber_type: 'Выберите тип абонента.',
            urgence: 'Выберите срочность.',
            team: {
                required: 'Выберите бригаду.',
                no_connection: 'Эта бригада не доступна для подлючения.'
            },
            phone: {
                digits: 'Введите только цифры.',
                no_phone: 'Введите номер телефона.'
            },
            address: 'Введите адрес.',
            description: 'Введите описание.',
            reason: 'Выберите причину.',
            account: 'Введите только цифры.',
            solution: 'Введите решение.',
        },
    });
}

function submitTicket() {
    $('#id_solution').removeClass('required');
    $('#id_reason').removeClass('required');
    if ($("#ticket").valid()) {
        $('#ticket').submit();
    }
}

function closeTicket() {
    $('#id_solution').addClass('required');
    $('#id_reason').addClass('required');
    if ($('#ticket').valid()) {
        $('#id_status').val(0);
        $('#ticket').submit();
    }
}

function cancelTicket() {
    $('#id_solution').addClass('required');
    $('#id_reason').addClass('required');
    if ($('#ticket').valid()) {
        $('#id_status').val(2);
        $('#ticket').submit();
    }
}

$(function() {
    minutes_settings = {
        stepMinute: 30,
    };
    $('#id_date_assigned').datetimepicker(minutes_settings);
    if (api_available) {
        $('<a class="additional_action" href="javascript:getSubscriberData()">Загрузить данные</a>').insertAfter($('#id_account'));
    }    
    $('<a class="additional_action" href="javascript:openMap()">Открыть карту</a>').insertAfter($('#id_address'));
    $('#id_time').timepicker(minutes_settings);
    validateForm();
    if (message) {
        displayMessage(message.message, message.error);
    }
});

function openMap() {
    function removeAppartment(address) {
        x = address.indexOf(', кв.');
        if (x != -1) {
            return address.substring(0, x);
        } else {
            return address;
        }
    }
    address = $('#id_address').val();
    address = removeAppartment(address);
    window.open('https://maps.google.ru/maps?q=' + city + ', ' + address);
}

function getSubscriberData() {
    var account = $('#id_account').val();
    var type = parseInt($('#id_subscriber_type').val());
    if (account === '') {
        displayMessage('Введите номер договора');
        return;
    }
    if (type !== 1 && type !== 2) {
        displayMessage('Выберите тип абонента');
        return;
    }
    console.log('test');
    $.post(subscriber_data_url, {account: account, type: type},
        function(data) {
            console.log('test1');
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
        displayMessage('Ошибка получения данных', true);
    });
}
