M.AutoInit();

document.addEventListener('DOMContentLoaded', function() {
    const navDropdown = document.querySelectorAll('.dropdown-trigger');
    const instances = M.Dropdown.init(navDropdown, ({
    alignment:'left',
    'hover':false,
    'constrainWidth':false,
    'coverTrigger':false
    }));

    var minDelivery = new Date()
    minDelivery.setDate(minDelivery.getDate() + 1)
    const datepickerElems = document.querySelectorAll('.datepicker');
    const datepickerOptions = {
        disableWeekends: true,
        minDate: minDelivery,
        autoClose: true,
        showClearBtn: true,
    }
    const datepickerInstances = M.Datepicker.init(datepickerElems, datepickerOptions);
});