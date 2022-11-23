M.AutoInit();

document.addEventListener('DOMContentLoaded', function() {
    var navDropdown = document.querySelectorAll('.dropdown-trigger');
    var instances = M.Dropdown.init(navDropdown, ({alignment:'left','hover':true, 'constrainWidth':false, 'coverTrigger':false}));
});