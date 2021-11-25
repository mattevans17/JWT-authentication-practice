$(document).ready(function() {
    $('#login_form').submit(function(event) {
        event.preventDefault()
        $.ajax({
            url: '/login',
            type: "POST",
            data: $(this).serialize(),
            success: function(data) {
                if (data.status === 'success') {
                    localStorage.setItem('access_token', data.access_token)
                    window.location.replace('/')
                } else {
                    alert(data.message)
                }
            }
        })
    })

    $('#register_form').submit(function(event) {
        event.preventDefault()
        $.ajax({
            url: '/register',
            type: "POST",
            data: $(this).serialize(),
            success: function(data) {
                localStorage.setItem('access_token', data.access_token)
                window.location.replace('/')
            }
        })
    })

    function refresh_tokens() {
        alert('refresh tokens...')
        $.ajax({
            url: '/refresh_tokens',
            type: "GET",
            success: function(data) {
                if (data.status === 'success') {
                    localStorage.setItem('access_token', data.access_token)
                } else {
                    alert(data.message)
                    window.location.replace('/login')
                }
            }
        })
    }

    $('#get_cars_button').click(function() {
        $.ajax({
            url: '/get_data',
            type: "GET",
            beforeSend: function (xhr) {
                xhr.setRequestHeader (
                    "Authorization",
                    localStorage.getItem('access_token')
                )
            },
            success: function(data) {
                for (const car of data.cars) {
                    $("#cars").append(
                        `<p>${car.brand} ${car.model}</p>`
                    )
                }
            },
            error: function (data) {
                if (data.status === 403) {
                    refresh_tokens()
                }
            }
        })
    })
})