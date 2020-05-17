const animateHeightX = document.querySelectorAll('.animateHeightX')
const cartCards = document.querySelectorAll('#cartCard')
for (let cartCard of cartCards) {
    let counter = 0;
    tlMax.fromTo(cartCard, .3, { y: '50', opacity: 0 }, { y: '0', opacity: 1, ease: Power2.ease }, `-=${counter}`);
    counter += 1;
}

tlMax.fromTo(animateHeightX, 2, { height: '0', opacity: 0 }, { height: '100%', opacity: 1, ease: Power2.easeInOut }, "-=1.3")

var countDownDate = new Date("August 5, 2020 23:00:00").getTime();

var x = setInterval(function() {

    var now = new Date().getTime();
    var distance = countDownDate - now;

    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    document.getElementById("deadline").innerHTML = days + "d " + hours + "h " +
        minutes + "m " + seconds + "s ";

    if (distance < 0) {
        clearInterval(x);
        document.getElementById("deadline").innerHTML = "EXPIRED";
    }
}, 1000);

$(document).ready(function() {
    $('.modal').modal();
});

let formaX = document.querySelector('#formaX');
let buyAn = document.querySelector('#buyAn');
buyAn.addEventListener("click", () => {
    if (formaX.style.display == "block") {
        formaX.style.display = "none";
    } else {
        formaX.style.display = "block"
    }
})