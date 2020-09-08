$(document).ready(() => {
    const DOMStrings = {
        loginForm : $('.form'),
        emailField: $('#email'),
        passwordField: $('#password'),

        errorText: $('.error-text'),
    }

    DOMStrings.loginForm.on('submit', (e) => {
        e.preventDefault()

        $.post('', 
        {
            email: $(DOMStrings.emailField).val(),
            password: $(DOMStrings.passwordField).val()
        }, (data) => {
            console.log(data.url)
            window.location.href = data.url;
        })
    })

})