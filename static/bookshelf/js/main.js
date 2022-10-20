document.addEventListener('DOMContentLoaded', function(){
    /* открытие и закрытие поиска */
    const searchTablet = document.querySelector('.header__search-container-tablet');
    const searchBtn = document.querySelector('.header__search-btn');
    const closeSearchBtn = document.querySelector('.header__search-close-btn');
    let searchWidth = 200;
  
    function searchWidthCalc() {
      if (document.documentElement.scrollWidth <= 500) {
        searchWidth = document.querySelector('.header__nav').offsetWidth;
      }
      else if(document.documentElement.scrollWidth <= 600) {
        searchWidth = document.querySelector('.header__nav').offsetWidth;
      }
      else if(document.documentElement.scrollWidth <= 830) {
        searchWidth = 342;
      }
      else if(document.documentElement.scrollWidth <= 1300) {
        searchWidth = 250;
      }
      else if(document.documentElement.scrollWidth > 1300) {
        searchWidth = 200;
      }
    }
  
    function searchOpen() {
      if (searchTablet.classList.contains('visible')) {
        searchTablet.classList.remove('visible')
  
        gsap.fromTo('.header__search-container-tablet',{
          width: searchWidth,
          display: "flex"
        },{
          width: 0,
          display: "none"
        });
  
        gsap.fromTo('.header__search-close-btn',{
          width: 23,
          display: "block"
        },{
          width: 0,
          display: "none"
        });
      }
      else {
        searchTablet.classList.add('visible');
  
        gsap.fromTo('.header__search-container-tablet.visible',{
          width: 0,
          display: "none"
        },{
          width: searchWidth,
          display: "flex"
        });
  
        gsap.fromTo('.header__search-close-btn',{
          width: 0,
          display: "none"
        },{
          width: 23,
          display: "block"
        });
      }
    }
  
    /*--------------------------------------------------------------------*/
  
    /* открытие и закрытие информации на карте */
    const closeInfoMapBtn = document.querySelector('.contacts__map-info-close-btn');
    const mapInfo = document.querySelector('.contacts__map-info');
  
    function closeInfoMap() {
      mapInfo.classList.remove('visible');
      gsap.to('.contacts__map-info',{
        x: -800,
        display: "none"
      });
    };
    /*--------------------------------------------------------------------*/
  
    /* открытие и закрытие бургер меню */
    const body = document.querySelector('body');
    const html = document.querySelector('html');
    const burgerBtn = document.querySelector('.header-bottom__burger');
    const burgerMenu = document.querySelector('.header-bottom__nav-mobile');
    const burgerMenuClose = document.querySelector('.nav-mobile__close-btn');
  
    function burgerMenuOpenAnimation() {
      if (!burgerMenu.classList.contains('burger-menu--is-open')) {
        burgerMenu.classList.add('burger-menu--is-open');
        body.classList.add('overflow--lock');
        html.classList.add('overflow--lock');
  
        gsap.fromTo('.header-bottom__nav-mobile.burger-menu--is-open',{
          x: -500,
          display: "none"
        },{
          x: 0,
          display: "block"
        });
      }
      else {
        burgerMenu.classList.remove('burger-menu--is-open');
        body.classList.remove('overflow--lock');
        html.classList.remove('overflow--lock');
  
        gsap.fromTo('.header-bottom__nav-mobile',{
          x: 0,
          display: "block"
        },{
          x: -500,
          display: "none"
        });
      }
    }
  
    function checkBurgerWidth() {
      if (document.documentElement.scrollWidth > 500 && burgerMenu.classList.contains('burger-menu--is-open')) {
        burgerMenuOpenAnimation();
      }
    }
    /*--------------------------------------------------------------------*/
  
    // плавный скролл
    const anchors = document.querySelectorAll('.nav-mobile__list-item-link');
  
    for (let anchor of anchors) {
      anchor.addEventListener('click', function(event){
        event.preventDefault();
        burgerMenuOpenAnimation();
  
        const blockID = anchor.getAttribute('href');
        document.querySelector('' + blockID).scrollIntoView({
          behavior: "smooth",
          block: "start"
        })
      });
    }
    /*--------------------------------------------------------------------*/
  
    /* обработчики событий */
    searchBtn.addEventListener('click', searchOpen);
    closeSearchBtn.addEventListener('click', searchOpen);
    closeInfoMapBtn.addEventListener('click', closeInfoMap);
    burgerBtn.addEventListener('click', burgerMenuOpenAnimation);
    burgerMenuClose.addEventListener('click', burgerMenuOpenAnimation);
  
    searchWidthCalc();
    window.addEventListener('resize', searchWidthCalc, true);
    window.addEventListener('resize', checkBurgerWidth, true);
  });