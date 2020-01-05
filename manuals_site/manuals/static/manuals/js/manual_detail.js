addSlashes();

function addSlashes() {
    // add trailing slashes to manual header when multiple admins are assigned to a manual
    let admins = document.getElementsByClassName('admin-assigned');
    if (admins.length > 1) {
        for (let i = 0; i < admins.length; i++) {
            admins[i].classList.add('admin-link');
        }
    }
}