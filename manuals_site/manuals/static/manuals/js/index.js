
scanDirectory();

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