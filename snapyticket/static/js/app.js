const header = document.querySelectorAll('header')
const animateLeft = document.querySelectorAll('.animateLeft')
const animateRight = document.querySelectorAll('.animateRight')
const animateBottom = document.querySelectorAll('.animateBottom')
const animateSearch = document.querySelector('.animateSearch')
const animateFade = document.querySelectorAll('.animateFade')
const searchBox = document.querySelectorAll('#search')
const animateHeight = document.querySelectorAll('.animateHeight')
const scalerOne = document.querySelectorAll('#circleOne')
const scalerTwo = document.querySelectorAll('#circleTwo')
const tlMax = new TimelineMax()

tlMax.fromTo(header, 1, { y: '-550', opacity: 0 }, { y: '0', opacity: 1, ease: Power2.easeInOut })
    .fromTo(animateLeft, 1, { x: '-100', opacity: 0 }, { x: '0', opacity: 1 })
    .fromTo(animateRight, 1, { x: '100', opacity: 0 }, { x: '0', opacity: 1, ease: Power2.easeInOut }, "-=1.3")
    .fromTo(animateBottom, 1, { y: '50', opacity: 0 }, { y: '0', opacity: 1, ease: Power2.easeInOut }, "-=1.3")
    .fromTo(animateSearch, 1, {
        y: '-100px',
        opacity: 0
    }, { y: '-28px', opacity: 1, ease: Power2.easeInOut }, "-=1.3")
    .fromTo(animateHeight, 1, { height: '0%', opacity: 0 }, { height: '100%', opacity: 1, ease: Power2.easeInOut }, "-=2.3")


new fullpage("#fullpage", {
    scrollingSpeed: 1000,
    autoScrolling: true,
    navigation: true,
    verticalCentered: false,
    paddingTop: '0',
    navigationColor: 'white',
    onLeave: (origin, destination, direction) => {
        const section = destination.item;
        console.log(section)
        const header = section.querySelectorAll('header')
        const animateLeft = section.querySelectorAll('.animateLeft')
        const animateRight = section.querySelectorAll('.animateRight')
        const animateBottom = section.querySelectorAll('.animateBottom')
        const animateSearch = section.querySelector('.animateSearch')
        const animateFade = section.querySelectorAll('.animateFade')
        const animateWidthXS = section.querySelectorAll('.animateWidthXS')
        const animateHeight = section.querySelectorAll('.animateHeight')
        const scalerOne = section.querySelectorAll('#circleOne')
        const scalerTwo = section.querySelectorAll('#circleTwo')
        const tlMax = new TimelineMax()
        if (destination.index === 0) {
            tlMax.fromTo(header, 1, { y: '-550', opacity: 0 }, { y: '0', opacity: 1, ease: Power2.easeInOut })
                .fromTo(animateLeft, 1, { x: '-100', opacity: 0 }, { x: '0', opacity: 1 })
                .fromTo(animateRight, 1, { x: '100', opacity: 0 }, { x: '0', opacity: 1, ease: Power2.easeInOut }, "-=1.3")
                .fromTo(animateBottom, 1, { y: '50', opacity: 0 }, { y: '0', opacity: 1, ease: Power2.easeInOut }, "-=1.3")
                .fromTo(animateSearch, 1, {
                    x: '-100',
                    opacity: 0
                }, { opacity: 1, x: '0', ease: Power2.easeInOut }, "-=1.3")
                .fromTo(animateHeight, 1, { width: '0%', opacity: 0 }, { width: '100%', opacity: 1, ease: Power2.easeInOut }, "-=2.3")
        } else if (destination.index === 1) {
            tlMax.fromTo(scalerOne, 1, { transform: 'scale(0)', opacity: 0 }, { transform: 'scale(1)', opacity: 1, ease: Power2.easeInOut }, "-=2.3")
                .fromTo(scalerTwo, 1, { transform: 'scale(0)', opacity: 0 }, { transform: 'scale(1)', opacity: 1, ease: Power2.easeInOut }, "=-2.1")
                .fromTo(animateRight, 1, { x: '100', opacity: 0 }, { x: '0', opacity: 1, ease: Power2.easeInOut }, "-=1.3")
                .fromTo(animateBottom, 1, { y: '50', opacity: 0 }, { y: '0', opacity: 1, ease: Power2.easeInOut }, "-=1.3");

            searchCard = section.querySelectorAll('.cateCard')

            for (let cateCard of searchCard) {
                let counter = 0;
                tlMax.fromTo(cateCard, .1, { y: '50', opacity: 0 }, { y: '0', opacity: 1, ease: Power2.ease }, `-=${counter}`);
                counter += .1;
            }

        } else if (destination.index === 2) {

            xCards = section.querySelectorAll('.xCard');

            for (let xCard of xCards) {
                let xCounter = 0;
                tlMax.fromTo(xCard, .4, { y: '100', opacity: 0 }, { y: '0', opacity: 1, ease: Power2.ease }, `-=${xCounter}`);
                xCounter += .1;
            }
        } else if (destination.index == 3) {
            tlMax.fromTo(animateBottom, 1, { y: '50', opacity: 0 }, { y: '0', opacity: 1, ease: Power2.easeInOut }, "-=1.3")
                .fromTo(animateWidthXS, 1, { width: '0', opacity: 0 }, { width: '25%', opacity: 1, ease: Power2.easeInOut }, "-=1.3", )
        }
    }
});

$(document).ready(function() {
    $('.carousel').carousel({});
    $('.modal').modal();
    $('select').formSelect({
        'origin': 'top',
    });
    $('.owl-carousel').owlCarousel({
        responsiveClass: true,
        rewind: true,
        responsive: {
            0: {
                items: 1,
                nav: true,
                stagePadding: 24,
            },
            600: {
                items: 2,
                nav: false,
            },
            1000: {
                items: 1,
                nav: true,
            }
        },
        margin: 10,
        loop: true,
        stagePadding: 44,
        lazyLoad: false,
        autoplay: true,
        autoplaySpeed: 1500,
        navSpeed: 1500,
    });
});


$(function() {
    $("#dashboard").load("templates/page_snippets/dashbaord.html' %}");
});

var instance = M.Carousel.getInstance('carousel');