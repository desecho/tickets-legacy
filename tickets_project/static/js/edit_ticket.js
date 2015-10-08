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
            type: 'Choose ticket type.',
            name: 'Enter name.',
            subscriber_type: 'Select subscriber type.',
            urgence: 'Select urgence.',
            team: {
                required: 'Select Team.',
                no_connection: "This team can't make connections."
            },
            phone: {
                digits: 'Input only digits.',
                no_phone: 'Enter phone number.'
            },
            address: 'Enter address.',
            description: 'Enter description.',
            reason: 'Select cause.',
            account: 'Input only digits.',
            solution: 'Enter solution.',
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
        displayMessage('Enter contract number');
        return;
    }
    if (type !== 1 && type !== 2) {
        displayMessage('Select subscriber type');
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