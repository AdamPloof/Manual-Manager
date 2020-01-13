
$(document).ready(function() {
    scanDirectory();
    getCurrentDir();
    showDropdowns();
    checkAdmin();
});


function getDirTable() {
    return document.getElementById('dir-table');
}


// Add an event listener to all folders and define the table to be refreshed.
function scanDirectory() {
    let folders = document.getElementsByClassName('folder');
    
    for(let i = 0; i < folders.length; i++) {
        folders[i].addEventListener("click", function(event) {
            // check if the button clicked has an event associated with it and if so stop the event
            if (event.cancelable) {
                event.preventDefault();
            }
            changeDir(this);
        })
    }
    
    allowNewDir();
}


// Add not-allowed to new-dir button if the dir_table is not present
function allowNewDir() {
    let dir_table = getDirTable();
    let new_dir_btn = document.getElementById('new-dir');
    
    if (!dir_table) {
        new_dir_btn.classList.toggle('not-allowed');
    }
    else if (new_dir_btn.classList.contains('not-allowed')) {
        new_dir_btn.classList.remove('not-allowed');
    }
    else {
        // pass
    }
}


// Change directory to selected folder
function changeDir(folder, opt_args = null) {
    
    // examples of folder id: "pk-1", "pk-4", etc.
    let dir_id = folder.id.slice(3);
    let dir_table = getDirTable();

    // opt_args will be a key/value object containing optional/alternative info
    // used for setting up for the XMLHttpRequest
    if (opt_args) {
        // pass
    }
    else {
        // pass
    }

    let requestURL = 'cd?dir_id=' + dir_id;

    let request = new XMLHttpRequest();

    request.open('GET', requestURL, true);
    request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

    request.responseType = 'text';

    request.onload = function() {

        // output will be the contents of the directory table
        let output = request.response;
        
        if(request.status == 200) {

            clearTable();

            dir_table.innerHTML = output;

            scanDirectory();
            getCurrentDir();
            showDropdowns();
        }
        else {
            console.log('Could not retrieve anything');
        }
    }

    request.send();

}


// Clears the current contents the directory table
function clearTable() {
    let dir_table = getDirTable()
    while (dir_table.firstChild) {
        dir_table.firstChild.remove();
    }
}


// Update the current directory id for use in the create-folder form
function getCurrentDir() {
    let dir_table = getDirTable()

    if (dir_table) {
        let current_folder = document.getElementsByClassName('file-root')[0];
        let dir_id = current_folder.id.slice(3);
        newManualDir(dir_id);
        initModals(dir_id);
    }
}


// Update the new manual link to include ?current-dir= param
function newManualDir(current_dir) {
    let new_manual_btn = document.getElementById("new-manual");
    let url = new URL(new_manual_btn.href);

    if (!url.search) {
        let query_string = "?current_dir=" + current_dir;
        new_manual_btn.href +=query_string;
    }
    else {
        console.log(url);
        let query_string = url.search;
        let search_params = new URLSearchParams(query_string);
        search_params.set('current_dir', current_dir);
        url.search = search_params.toString();
        new_manual_btn.href = url.toString();
    }
}


// Add a listener to the new-dir button and call the modal when clicked
function initModals(dir_id) {

    // Call the modal form to Create new folder
    $("#new-dir").modalForm({
        formURL: "manual/new-folder?dir_id=" + dir_id
    });

    // Call the modal form to Update folder
    $(".folder-update").each(function() {
        let node = $(this).data('pk');
        $(this).modalForm({formURL: $(this).data('id') + "?dir_id=" + dir_id + "&node=" + node});
    });

    // Call the modal form to Add Favorite for folder
    $(".folder-add-fav").click(function() {
        let fav_id = $(this).data('pk');
        let fav_name = $(this).data('id');
        let current_dir = $(this).data('loc');

        $('#fav-context').html(fav_name);
        $("#fav-modal").modal('show');

        postAddFav(fav_id, current_dir);
    });

    // Call the modal form to Delete folder
    $(".folder-delete").each(function() {
        let node = $(this).data('pk');
        $(this).modalForm({formURL: $(this).data('id') + "?dir_id=" + dir_id + "&node=" + node});
    });
}


// If user choose to save favorite then submit the fav-form
function postAddFav(fav_id, current_dir) {
    // Set the form input value to the be the pk of the favorite to add
    $('#fav-id').val(fav_id);

    // Add query string to the action url so that redirect goes to current folder
    let url = $('#fav-form').attr('action') + '?dir_id=' + current_dir;
    $('#fav-form').attr('action', url);

    // Submit the form
    $('#add-fav-btn').click(function() {
        $('#fav-form').submit();
    })
}

// Show the dropdown for update/delete folders
function showDropdowns() {
    let dropdownBtns = document.getElementsByClassName("btn-drop");

    for(let i = 0; i < dropdownBtns.length; i++) {
        dropdownBtns[i].addEventListener("click", function() {
            closeDropdowns();
            this.nextElementSibling.classList.toggle("show-drop");
        })
    }
  }
  

// Close all open drop downdowns
function closeDropdowns() {
    let dropdowns = document.getElementsByClassName("drop-menu");
    for (let i = 0; i < dropdowns.length; i++) {
      let openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show-drop')) {
        openDropdown.classList.remove('show-drop');
      }
    } 
}


  // Close the dropdown menu if the user clicks outside of it
  window.onclick = function(event) {
    if (!event.target.matches('.btn-drop')) {
      let dropdowns = document.getElementsByClassName("drop-menu");
      for (let i = 0; i < dropdowns.length; i++) {
        let openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show-drop')) {
          openDropdown.classList.remove('show-drop');
        }
      }
    }
  } 


function checkAdmin() {
    let adminTable = document.getElementById('admin-table');

    if (adminTable) {
        initAdminModals();
    }
}


function initAdminModals() {

    // Call the modal form to assign Manual
    $(".manual-assign").each(function() {
        $(this).modalForm({formURL: $(this).data('id')});
    });

     // Call the modal form to modify the next update for Manual
     $(".manual-next-update").each(function() {
        $(this).modalForm({formURL: $(this).data('id')});
    });

     // Call the modal form to archive Manual
     $(".manual-archive").each(function() {
        $(this).modalForm({formURL: $(this).data('id')});
        loadDatePicker();
    });

     // Call the modal form to delete the Manual
     $(".manual-admin-delete").each(function() {
        $(this).modalForm({formURL: $(this).data('id')});
    });
}


function loadDatePicker() {
    // Attach an event handler to Date input box
    $("#modal").on('focus', '#id_next_update', function() {
        $("#id_next_update").flatpickr();
    })  
}