// add row
    $("#addRow").click(function () {
        var html = '';
        html += '<div class="row mb-3" id="inputFormRow">';
        html += '<div class="col-sm-3" >';
        html += '<select class="form-select selectpicker form-control" name="field[]">';
        html += '<option value="first_name">first_name</option>';
        html += '<option value="last_name">last_name</option>';
        html += '<option value="personal_number">personal_number</option>';
        html += '<option value="birthdate">birthdate</option>';
        html += '<option value="address">address</option>';
        html += '<option value="county">county</option>';
        html += '<option value="phone_number">phone_number</option>';
        html += '<option value="mac_address">mac_address</option>';
        html += '<option value="ip_address">ip_address</option>';
        html += '<option value="job">job</option>';
        html += '<option value="iban">iban</option>';
        html += '<option value="currency">currency</option>';
        html += '<option value="balance">balance</option>';
        html += '<option value="latitude">latitude</option>';
        html += '<option value="longitude">longitude</option>';
        html += '</select>';
        html += '</div>';
        html += '<div class="col-sm-6">';
        html += '<input autocomplete="off" class="form-control m-input" name="field[]" placeholder="Enter field custom name" type="text">';
        html += '</div>';
        html += '<div class="col-sm-1">';
        html += '<button id="removeRow" type="button" class="btn btn-danger">×</button>';
        html += '</div>';
        html += '</div>';

        $('#newRow').append(html);
    });

    // remove row
    $(document).on('click', '#removeRow', function () {
        $(this).closest('#inputFormRow').remove();
    });