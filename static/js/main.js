var owlProduct;

$(document).ready(function () {
    let owlProduct = $('.owl-carousel');

    if (owlProduct.length > 0) {
        owlProduct.owlCarousel({
            loop: true,
            margin: 10,
            responsive: {
                0: {
                    items: 1
                }
            },
            mouseDrag: true,
            dotsContainer: '#box-carousel-dots'
        });
    }

    setTimeout(function () {
        var popup = document.getElementById('popup');
        popup = M.Modal.init(popup);
        popup.open();
    }, 2000); // Adjust the delay (in milliseconds) as per your requirement
});