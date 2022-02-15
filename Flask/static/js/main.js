const input = document.getElementById("checkbox")

document.body.setAttribute("data-theme", "light")

input.addEventListener('change', (e) =>{
    if(e.target.checked){
        document.body.setAttribute('data-theme', 'dark')
    }

    else{
        document.body.setAttribute('data-theme', 'light')
    }
})
