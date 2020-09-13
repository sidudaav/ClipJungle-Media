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

const addAlert = (alert) => {
    const html = `<li class="alert alert-${alert.type}"> <h3 class="alert-title">${alert.title}</h3><p class="alert-body">${alert.body}</p></li>`
    $('.alerts-list').prepend(html)

    const newAlert = $('.alerts-list li:first-child')
    setTimeout(() => {
        $(newAlert).hide()
    }, 5000)
}