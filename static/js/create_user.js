form = document.getElementById('signup')

form.addEventListener('submit',(e)=>{
    e.preventDefault()
    //let csrf = document.getElementById('csrf_token')
    //console.log(csrf)
    let username = document.getElementById('username').value
    let first_name = document.getElementById('first_name').value
    let last_name = document.getElementById('last_name').value
    let email = document.getElementById('email').value
    let phone = document.getElementById('phone').value
    let password = document.getElementById('password').value
    let password2 = document.getElementById('password2').value

    if (password != password2){
        document.getElementById('error').innerHTML = 'Your Passwords Do not Match'
    }else{
       document.getElementById('signup').submit() 
    }
})

let sendBack = async (username,first_name,last_name,email,phone,password) =>{  
    let response = await fetch('/sign_up/',{
        body:JSON.stringify({
            'username':username,
            'email': email,
            'first_name':first_name,
            'last_name':last_name,
            'phone':phone,
            'password':password,
    }),
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken":csrftoken
          }
    })
    if (response.status != 200){
        document.getElementById('error').innerHTML = 'This username has been taken'
    }
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}