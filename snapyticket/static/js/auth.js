$(document).ready(function() {
    $('.btnX').click(function() {
        $(this).addClass("activate")
    })
})

const nextForm = document.querySelector('#nextForm')
const backForm = document.querySelector('#backForm')
const loginForm = document.querySelector('#loginForm')
const submitForm = document.querySelector('#submitForm')
console.log(nextForm)

const username = document.querySelector('#id_username')
const email = document.querySelector('#id_email')
const phone = document.querySelector('#id_phone_0')
const password1 = document.querySelector('#id_password1')
const password2 = document.querySelector('#id_password2')
const labelUsername = document.querySelector('form p label[for="id_username"')
const labelEmail = document.querySelector('form p label[for="id_email"')
const labelPhone = document.querySelector('form p label[for="id_phone_0"')
const labelPassword2 = document.querySelector('form p label[for="id_password2"')
const labelPassword1 = document.querySelector('form p label[for="id_password1"')
const input = document.querySelectorAll('input')


nextForm.addEventListener("click", () => {
    if (username.value == "") {
        username.style.border = "1.5px solid #EB5757"
        labelUsername.style.color = "#EB5757"
        username.style.borderBottom = "1.5px solid #EB5757 !important"
    }
    if (email.value == "") {
        email.style.border = "1.5px solid #EB5757"
        labelEmail.style.color = "#EB5757"
        email.style.borderBottom = "1.5px solid #EB5757 !important"
    }
    if (phone.value == "") {
        phone.style.border = "1.5px solid #EB5757"
        labelPhone.style.color = "#EB5757"
        phone.style.borderBottom = "1.5px solid #EB5757 !important"
    } else {
        username.style.display = "none"
        labelUsername.style.display = "none"
        email.style.display = "none"
        labelEmail.style.display = "none"
        phone.style.display = "none"
        labelPhone.style.display = "none"
        password1.style.display = "block"
        labelPassword1.style.display = "block"
        password2.style.display = "block"
        labelPassword2.style.display = "block"
        nextForm.style.display = "none";
        backForm.style.display = "block";
        loginForm.style.display = "none";
        submitForm.style.display = "block";
    }
})