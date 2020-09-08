$(document).ready(() => {
    const DOMStrings = {
        loginForm : $('.login-form'),
        loginEmailField: $('#loginEmail'),
        loginPasswordField: $('#loginPassword'),

        registerForm : $('.register-form'),
        registerFirstNameField: $('#registerFirstName'),
        registerLastNameField: $('#registerLastName'),
        registerUsernameField: $('#registerUsername'),
        registerEmailField: $('#registerEmail'),
        registerPasswordField: $('#registerPassword'),
    }

    DOMStrings.loginForm.on('submit', (e) => {
        e.preventDefault()

        $.post("login/", 
        {
            email: $(DOMStrings.loginEmailField).val(),
            password: $(DOMStrings.loginPasswordField).val()
        }, (data) => {
            console.log(data.url)
            window.location.href = data.url;
        })
    })

    DOMStrings.registerForm.on('submit', e => {
        e.preventDefault()

        $.post('register/', 
        {
            firstName: $(DOMStrings.registerFirstNameField).val(),
            lastName: $(DOMStrings.registerLastNameField).val(),
            username: $(DOMStrings.registerUsernameField).val(),
            email: $(DOMStrings.registerEmailField).val(),
            password: $(DOMStrings.registerPasswordField).val()
        }, (data) => {
            if (data.status === 'OK') {
                $(DOMStrings.registerFirstNameField).val(''),
                $(DOMStrings.registerLastNameField).val(''),
                $(DOMStrings.registerUsernameField).val(''),
                $(DOMStrings.registerEmailField).val(''),
                $(DOMStrings.registerPasswordField).val('')
            }
        })
    })
})