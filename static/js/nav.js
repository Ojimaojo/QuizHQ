let mob_menu = document.getElementById('mob-menu')
let toggleBtn = document.getElementById('togglebtn')

toggleBtn.addEventListener('click', function(){
    if(mob_menu.classList.contains('hide')){
        mob_menu.classList.remove('hide')
        mob_menu.classList.add('show')
    }else{
        mob_menu.classList.remove('show')
        mob_menu.classList.add('hide')
    }
    
})