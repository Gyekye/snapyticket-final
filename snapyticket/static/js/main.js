const menuBtn = document.querySelector('.menu-btn');
const sidebar = document.querySelector('.sidebar')

setTimeout(() => {
    $('.mobile-preloader').fadeToggle()
}, 200);
setTimeout(() => {
    $('.messageBox').slideToggle()
}, 4000);

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