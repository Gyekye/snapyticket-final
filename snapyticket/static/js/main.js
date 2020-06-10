const menuBtn = document.querySelector('.menu-btn');
const sidebar = document.querySelector('.sidebar')

setTimeout(() => {
    $('.mobile-preloader').fadeToggle()
}, 200);
setTimeout(() => {
    $('.messageBox').slideToggle()
}, 4000);
setTimeout(() => {
    $('.messageBox-overlay').slideToggle()
}, 4000);

$(document).ready(() => {
    $('.sidenav').sidenav();
    $('.materialboxed').materialbox();
    $('.dropdown-trigger').dropdown();
    $('.collapsible').collapsible();
    $('.tabs').tabs();
    $('.modal').modal();
    $(".owl-carousel.most-featured").owlCarousel({
        loop: true,
        margin: 20,
        items: 1,
        stagePadding: 40,
        center: false,
        rtl: false,
        merge: true,
        autoplay: true,
        autoplaySpeed: 2000,
        autoplayTimeout: 5000,
        autoplayHoverPause: true
    });
    $(".owl-carousel.featured").owlCarousel({
        loop: true,
        margin: 15,
        items: 2,
        stagePadding: 30,
        center: false,
        rtl: false,
        merge: true,
        autoplay: true,
        autoplaySpeed: 1000,
        autoplayTimeout: 4000,
        autoplayHoverPause: true
    });
    $(".owl-carousel.category").owlCarousel({
        loop: true,
        margin: 10,
        items: 3,
        stagePadding: 0,
        center: false,
        rtl: false,
        merge: true,
        autoplay: true,
        autoplaySpeed: 1000,
        autoplayTimeout: 4000,
        autoplayHoverPause: true
    });
})

let menuOpen = false;
menuBtn.addEventListener("click", () => {
    if (!menuOpen) {
        menuBtn.classList.add('openMenu');
        menuOpen = true;
        sidebar.classList.add('openSidebar')
    } else {
        menuBtn.classList.remove('openMenu');
        menuOpen = false;
        sidebar.classList.remove('openSidebar')
    }
})

const nextSec = document.querySelector('#nextSec')
const nextSecX = document.querySelector('#nextSecX')
const nextSection = document.querySelector('.nextSection')
const nextSectionX = document.querySelector('.nextSectionX')
const closerNextA = document.querySelector('.closerNextA')
const closerNextB = document.querySelector('#closerNextB')

nextSecX.addEventListener("click", () => {
    nextSectionX.style.transform = 'translateX(0%)'
})

closerNextA.addEventListener("click", () => {
    nextSection.style.transform = 'translateX(100%)'
})

closerNextB.addEventListener("click", () => {
    nextSectionX.style.transform = 'translateX(100%)'
})

nextSec.addEventListener("click", () => {
    nextSection.style.transform = 'translateX(0%)'
})