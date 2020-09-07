var csrftoken = $.cookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));

}

// Sets up AJAX
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(() => {
    const DOMStrings = {
        registrationForm : $('.form'),
        firstNameField: $('#firstName'),
        lastNameField: $('#lastName'),
        usernameField: $('#username'),
        emailField: $('#email'),
        passwordField: $('#password'),
    }

    DOMStrings.registrationForm.on('submit', e => {
        e.preventDefault()
        console.log('submitted!')

        $.post('', 
        {
            firstName: $(DOMStrings.firstNameField).val(),
            lastName: $(DOMStrings.lastNameField).val(),
            username: $(DOMStrings.usernameField).val(),
            email: $(DOMStrings.emailField).val(),
            password: $(DOMStrings.passwordField).val()
        }, (data) => {
            if (data.status === 'OK') {
                $(DOMStrings.firstNameField).val(''),
                $(DOMStrings.lastNameField).val(''),
                $(DOMStrings.usernameField).val(''),
                $(DOMStrings.emailField).val(''),
                $(DOMStrings.passwordField).val('')
            }
        })
    })
})