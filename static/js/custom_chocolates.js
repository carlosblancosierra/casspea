$(document).ready(function () {
  const selectBackground = $('#select-background')
  const customTopBackground = $('#custom-top-background')
  const customSideBackground = $('#custom-side-background')

  const selectLayer1 = $('#select-layer-1')
  const customTopLayer1 = $('#custom-layer-1')
  const customSideLayer1 = $('#custom-side-layer-1')

  const selectLayer2 = $('#select-layer-2')
  const customTopLayer2 = $('#custom-layer-2')
  const customSideLayer2 = $('#custom-side-layer-2')


  const selectLayer3 = $('#select-layer-3')
  const customTopLayer3 = $('#custom-layer-3')
  const customSideLayer3 = $('#custom-side-layer-3')


  selectBackground.change(function () {
    const images = JSON.parse(selectBackground.val())

    customTopBackground.fadeTo(0, 0)
    customSideBackground.fadeTo(0, 0)

    if (images) {
      customTopBackground.attr('src', images['top']);
      customSideBackground.attr('src', images['side']);
      customTopBackground.fadeTo("medium", 1)
      customSideBackground.fadeTo("medium", 1)
    }


  });

  selectLayer1.change(function () {
    var images = selectLayer1.val()

    customTopLayer1.fadeTo(0, 0)
    customSideLayer1.fadeTo(0, 0)
    if (images) {
      images = JSON.parse(images)
      customTopLayer1.attr('src', images['top']);
      customSideLayer1.attr('src', images['side']);

      customTopLayer1.fadeTo("medium", 1)
      customSideLayer1.fadeTo("medium", 1)
    }
  });

  selectLayer2.change(function () {
    var images = selectLayer2.val()
    customTopLayer2.fadeTo(0, 0)
    customSideLayer2.fadeTo(0, 0)
    if (images) {
      images = JSON.parse(images)
      customTopLayer2.attr('src', images['top']);
      customSideLayer2.attr('src', images['side']);

      customTopLayer2.fadeTo("medium", 1)
      customSideLayer2.fadeTo("medium", 1)
    }
  });

  selectLayer3.change(function () {
    var images = selectLayer3.val()
    customTopLayer3.fadeTo(0, 0)
    customSideLayer3.fadeTo(0, 0)
    if (images) {
      images = JSON.parse(images)
      customTopLayer3.attr('src', images['top']);
      customSideLayer3.attr('src', images['side']);
      customTopLayer3.fadeTo("medium", 1)
      customSideLayer3.fadeTo("medium", 1)
    }
  });
});










// $(document).ready(function () {
//   const selectBackground = $('#select-background')
//   const customBackground = $('#custom-top-background')

//   const selectLayer1 = $('#select-layer-1')
//   const customTopLayer1 = $('#custom-layer-1')
//   const customSideLayer1 = $('#custom-side-layer-1')

//   const selectLayer2 = $('#select-layer-2')
//   const customTopLayer2 = $('#custom-layer-2')

//   const selectLayer3 = $('#select-layer-3')
//   const customTopLayer3 = $('#custom-layer-3')

//   customTopLayer1.fadeTo(0, 0)
//   // customTopLayer2.css('opacity') = 0
//   // customTopLayer3.css('opacity') = 0

//   selectBackground.change(function () {
//     customBackground.fadeTo(0, 0)
//     const value = selectBackground.val()
//     console.log(value)
//     customBackground.attr('src', value);
//     customBackground.fadeTo("medium", 1)
//   });

//   selectLayer1.change(function () {
//     customTopLayer1.fadeTo(0, 0)
//     customTopLayer1.attr('src', selectLayer1.val());
//     customTopLayer1.fadeTo("medium", 1)
//   });

//   selectLayer2.change(function () {
//     customTopLayer2.fadeTo(0, 0)
//     customTopLayer2.attr('src', selectLayer2.val());
//     customTopLayer2.fadeTo("medium", 1)
//   });

//   selectLayer3.change(function () {
//     customTopLayer3.fadeTo(0, 0)
//     const value = selectLayer3.val()
//     customTopLayer3.attr('src', value);
//     if (value) { customTopLayer3.fadeTo("medium", 1) }
//   });
// });