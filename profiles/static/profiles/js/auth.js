$(document).ready(() => {
    // Collect DOM Strings for all relevant elements
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

    // Clears the Error Messages
    const clearErrorMessages = () => {
        const errorMessages = $('.error-message').toArray()
        errorMessages.forEach(errorMessage => {
            $(errorMessage).text('')
            $(errorMessage).css({
                'display': 'none',
            })
        })
    }

    // Clears the Input Fields
    const clearInputFields = () => {
        const inputFields = $('input.form-control').toArray()
        inputFields.forEach(inputField => {
            $(inputField).val('')
        })
    }

    const displayErrorMessage = (fld, msg) =>{
        const parent = fld.parent()
        const errorMessage = $(parent).find('.error-message')
        
        $(errorMessage).css({
            'display': 'block',
        })

        $(errorMessage).text(msg)
    }

    // Validate Username for registration
    const validateUsername = fld => {
        let msg = ''
        const illegalChars = /\W/ // allow letters, numbers, and underscores
        const val = $(fld).val()

        if (val == '') {
            msg = 'Username Is Empty'
            displayErrorMessage($(fld), msg)

            return false
        } else if (val.length < 5 || val.length > 15) {
            msg = val.length < 5 ? 'Username Is Too Short' : 'Username Is Too Long'
            displayErrorMessage($(fld), msg)

            return false
        } else if (illegalChars.test(val)) {            
            msg = 'Username Contains Illegal Characters'
            displayErrorMessage($(fld), msg)

            return false        
        }

        return true
    }

    // Validate First Name for registration
    const validateFirstName = fld => {
        let msg = ''
        const illegalChars = /\W/ // allow letters, numbers, and underscores
        const val = $(fld).val()

        if (val == '') {
            msg = 'First Name Is Empty'
            displayErrorMessage($(fld), msg)

            return false
        } else if (illegalChars.test(val)) {            
            msg = 'First Name Contains Illegal Characters'
            displayErrorMessage($(fld), msg)

            return false        
        }

        return true
    }

    // Validate Last Name for registration
    const validateLastName = fld => {
        let msg = ''
        const illegalChars = /\W/ // allow letters, numbers, and underscores
        const val = $(fld).val()

        if (val == '') {
            msg = 'Last Name Is Empty'
            displayErrorMessage($(fld), msg)

            return false
        } else if (illegalChars.test(val)) {            
            msg = 'Last Name Contains Illegal Characters'
            displayErrorMessage($(fld), msg)

            return false        
        }

        return true
    }

    // Show password when textbox is clicked
    console.log($('#showPassword'))
    $('#showPassword').on('click', () => {
        if ($(DOMStrings.registerPasswordField).attr('type') === "password") {
          $(DOMStrings.registerPasswordField).attr('type', 'text');
        } else {
          $(DOMStrings.registerPasswordField).attr('type', 'password');
        }
    })

    // Handle submit for login form
    DOMStrings.loginForm.on('submit', (e) => {
        e.preventDefault()

        clearErrorMessages()

        $.post("login/", 
        {
            email: $(DOMStrings.loginEmailField).val(),
            password: $(DOMStrings.loginPasswordField).val()
        }, (data) => {
            if (data.status === 'KO') {
                if (data.errorField === 'Email') {
                    displayErrorMessage($(DOMStrings.loginEmailField), data.msg)
                } else if (data.errorField === 'Password') {
                    displayErrorMessage($(DOMStrings.loginPasswordField), data.msg)
                }
            } else if (data.status === 'OK') {
                clearInputFields()
                window.location.href = data.url;
            }
        })
    })

    // Handle submit for register form
    DOMStrings.registerForm.on('submit', e => {
        e.preventDefault()

        clearErrorMessages()

        if (!validateFirstName(DOMStrings.registerFirstNameField) ||
            !validateLastName(DOMStrings.registerLastNameField) ||
            !validateUsername(DOMStrings.registerUsernameField)) {
            return null
        }

        $.post('register/', 
        {
            firstName: $(DOMStrings.registerFirstNameField).val(),
            lastName: $(DOMStrings.registerLastNameField).val(),
            username: $(DOMStrings.registerUsernameField).val(),
            email: $(DOMStrings.registerEmailField).val(),
            password: $(DOMStrings.registerPasswordField).val()
        }, (data) => {
            if (data.status === 'KO') {
                if (data.errorField === 'Email') {
                    displayErrorMessage($(DOMStrings.registerEmailField), data.msg)
                } else if (data.errorField === 'Username') {
                    displayErrorMessage($(DOMStrings.registerUsernameField), data.msg)
                }
            } else if (data.status === 'OK') {
                clearInputFields()
                addAlert({
                    'type': 'success',
                    'title': 'Registration Successful',
                    'body': 'You may now log in'
                })            
            }
        })
    })
})