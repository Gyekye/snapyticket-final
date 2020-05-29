const menuBtn = document.querySelector('.menu-btn');
let menuOpen = false;
menuBtn.addEventListener("click", () => {
    if (!menuOpen) {
        menuBtn.classList.add('openMenu');
        menuOpen = true;
    } else {
        menuBtn.classList.remove('openMenu');
        menuOpen = false;
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