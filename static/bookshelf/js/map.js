// import width from './test.js'
// console.log(width);

ymaps.ready(init);
function init(){
  var myMap = new ymaps.Map("map", {
    center: [59.938955, 30.315644],
    controls: [],
    zoom: 13,
  });

  const myGeoObject = new ymaps.GeoObject({
    geometry: {
      type: "Point",
      coordinates: [55.76948022, 37.63891581]
    }
  });

  myPlacemark = new ymaps.Placemark([59.938955, 30.315644], {
    hintContent: 'г. Санкт-Петербург'
  },{
    iconLayout: 'default#image',
    iconImageHref:'/static/bookshelf/img/placemark.svg',
    iconImageSize: [12, 12],
    iconImageOffset: [0, 0]
  }),
  myPlacemark.events.add('click', function () {
    if (!document.querySelector('.contacts__map-info').classList.contains('visible')) {
      document.querySelector('.contacts__map-info').classList.add('visible');
      gsap.fromTo('.contacts__map-info',{
        x: -800,
        display: "none"
      },{
        x: 0,
        display: "block"
      });
    }
  })

  myMap.geoObjects.add(myPlacemark);                                            /* добавление метки */
  myMap.behaviors.disable([
    'scrollZoom', 'dblClickZoom', 'multiTouch', 'rightMouseButtonMagnifier',    /* полное отключение зума карты */
    'leftMouseButtonMagnifier'
  ]);
  myMap.behaviors.disable('drag');                                              /* полное отключение перетаскивания карты на телефонах */
}