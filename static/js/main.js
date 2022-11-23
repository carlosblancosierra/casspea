var owlProduct;

$(document).ready(function () {
  let owlHomeBanner = $('#home-carousel').owlCarousel({
    loop: true,
    margin: 0,
    nav: true,
    responsive: {
      0: {
        items: 1
      }
    },
  })

  let owlCarouselGallery = $('#home-carousel-gallery').owlCarousel({
    loop: true,
    margin: 0,
    nav: true,
    responsive: {
      0: {
        items: 1
      }
    },
  })
});