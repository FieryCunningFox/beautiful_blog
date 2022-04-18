var csrf = document.getElementById('csrf').value

function login() {
    var username = documment.getElementById('login_username');
    var password = documment.getElementById('login_password');

    if (username == '' && password == '') {
        alert('You must enter a username and password')
    }

    var data = {
        'username' : username,
        'password' : password
    }

    fetch('api/login', {
        method : 'POST',
        headers : {
            'Content-Type': 'application/json',
            'X-CSRFToken' : csrf,
        },
        'body' : JSON.stringify(data)
    }).then(result => result.json())
    .then(response => {
        console.log()

        if (response.status == 200) {
            window.location.reload('/')
        }
        else {
            alert(response.message)
        }
    })
}