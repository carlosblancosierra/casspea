$(document).ready(function () {
  const flavourCheckboxes = $('.flavour-checkbox')
  const quantitySelect = $('#quantity-select')
  const remainingFlavours = $('#remaining-flavours')
  const submitBtn = $('#submit-btn-custom-chocolates')
  const prebuildCheckboxes = $('.prebuild-checkbox')
  var max_flavours = 0

  quantitySelect.on('change', function() {
    max_flavours = quantitySelect.find('option:selected').data('max-flavours');
    remainingFlavours.text(max_flavours);
    flavourCheckboxes.prop('checked', false);
    flavourCheckboxes.prop('disabled', false);
  });

  prebuildCheckboxes.on('change', function() {
   var numChecked = prebuildCheckboxes.filter(':checked').length;
   if (numChecked > 0){
    submitBtn.prop('disabled', false);
   } else if (numChecked === 0){
   submitBtn.prop('disabled', true);
   }
  });

  flavourCheckboxes.each(function() {
      $(this).on('change', function() {
        var numChecked = flavourCheckboxes.filter(':checked').length;
        if (numChecked === max_flavours){
            flavourCheckboxes.not(':checked').prop('disabled', true);
            submitBtn.prop('disabled', false);
        } else if (numChecked === 0){
            submitBtn.prop('disabled', true);
        } else {
            flavourCheckboxes.not(':checked').prop('disabled', false);
            submitBtn.prop('disabled', false);
        }
      });
    });
});






