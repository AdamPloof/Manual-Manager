
$(document).ready(function() {
    scanDirectory();
    getCurrentDir();
});

// Add an event listener to all folders a define the table to be refreshed.
function scanDirectory() {
    var folders = document.getElementsByClassName('folder');
    var dir_table = document.getElementById('dir-table');

    for(let i = 0; i < folders.length; i++) {
        folders[i].addEventListener("click", function(event) {
            // check if the button clicked has an event associated with it and if so stop the event
            if (event.cancelable) {
                event.preventDefault();
            }
            changeDir(this, dir_table);
        })
    }
}

// Change directory to selected folder
function changeDir(folder, dir_table) {
    
    // examples of folder id: "pk-1", "pk-4", etc.
    let dir_id = folder.id.slice(3);
    let requestURL = 'cd?dir_id=' + dir_id;

    let request = new XMLHttpRequest();

    request.open('GET', requestURL, true);
    request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

    request.responseType = 'text';

    request.onload = function() {

        // output will be the contents of the directory table
        let output = request.response;
        
        if(request.status == 200) {

            clearTable(dir_table);

            dir_table.innerHTML = output;

            scanDirectory();
            getCurrentDir();
        }
        else {
            console.log('Could not retrieve anything');
        }
    }

    request.send();

}

// Clears the current contents the directory table
function clearTable(myTable) {
    while (myTable.firstChild) {
        myTable.firstChild.remove();
    }
}

// Update the current directory id for use in the create-folder form
function getCurrentDir() {
    let current_folder = document.getElementsByClassName('file-root')[0];
    let dir_id = current_folder.id.slice(3);
    initModals(dir_id);
}

// Add a listener to the new-dir button and call the modal when clicked
function initModals(dir_id) {

    // Call the modal form to Create new folder
    $("#new-dir").modalForm({
        formURL: "manual/new-folder?dir_id=" + dir_id
    });

    // Call the modal form to Update folder
    $(".folder-update").each(function() {
        $(this).modalForm({formURL: $(this).data('id') + "?dir_id=" + dir_id});
    });

    // Call the modal form to Delete folder
    $(".folder-delete").each(function() {
        $(this).modalForm({formURL: $(this).data('id') + "?dir_id=" + dir_id});
    });
}