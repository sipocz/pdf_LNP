let darkMode = localStorage.getItem('darkMode')
const darkModeToggle = document.querySelector('#button')

const darkmodeIcon = "bi bi-moon"
const lightmodeIcon = "bi bi-brightness-high-fill"
const icon = document.getElementById("switcher");
icon.className = lightmodeIcon;


const enableDarkMode = () =>{
    document.body.classList.add('darkmode')
    localStorage.setItem('darkMode', 'enabled')
    icon.className=darkmodeIcon
}

const disableDarkMode = () =>{
    document.body.classList.remove('darkmode')
    localStorage.setItem('darkMode', null)
    icon.className=lightmodeIcon;
}

if(darkMode === "enabled"){
    enableDarkMode()
}

darkModeToggle.addEventListener("click", ()=>{
    darkMode = localStorage.getItem('darkMode')
    if(darkMode !== 'enabled'){
        enableDarkMode()
    }
    else{
        disableDarkMode()
    }
})
