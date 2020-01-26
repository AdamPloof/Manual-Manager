
$(document).ready(function() {
    scanDirectory();
    getCurrentDir();
    showDropdowns();
    checkModals();
});


$("#date-test").flatpickr();


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
            checkModals();
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

    // Call the modal form to Delete folder
    $(".folder-delete").each(function() {
        let node = $(this).data('pk');
        $(this).modalForm({formURL: $(this).data('id') + "?dir_id=" + dir_id + "&node=" + node});
    });
}


function checkModals() {
    // Determine which triggers need to be instantiated
    let adminTable = document.getElementById('admin-table');
    let fav_table = document.getElementById("fav-manual-table");
    let dir_table = getDirTable();

    if (adminTable) {
        initAdminModals();
    }
    else if (fav_table || dir_table) {
        initFavModals();
    }
}


function initFavModals() {

    // Call the modal form to Add/Remove Favorite for folder
    $(".folder-add-fav, .folder-remove-fav").click(function() {
        // Change the glyphicon in the modal to folder
        $("#fav-symbol").attr("class", "far fa-folder ms-2");
        let fav_type = "folder";
        getFavInfo(this, fav_type);
    });

    // Call the modal form to Add/Remove Favorite for file
    $(".file-add-fav, .file-remove-fav").click(function() {
        // Change the glyphicon in the modal to file
        $("#fav-symbol").attr("class", "far fa-file ms-2");
        let fav_type = "file";
        getFavInfo(this, fav_type);
    });
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
    });

     // Call the modal form to delete the Manual
     $(".manual-admin-delete").each(function() {
        $(this).modalForm({formURL: $(this).data('id')});
    });

    $(".manual-next-update").click(function() {
        loadDatePicker();
    })
    
}


function getFavInfo(fav_choice, fav_type) {
    let fav_id = $(fav_choice).data('pk');
    let fav_name = $(fav_choice).data('id');
    let current_dir = $(fav_choice).data('loc');

    $('#fav-context').html(fav_name);
    $("#fav-modal").modal('show');

    postFav(fav_id, current_dir, fav_type);
}


// If user choose to save favorite then submit the fav-form
function postFav(fav_id, current_dir, fav_type) {
    // Set the form input value to the be the pk of the favorite to add
    $('#fav-id').val(fav_id);

    // Add the type of fav to add (file or folder) to data-type on form input
    $('#fav-type').val(fav_type);
   
    // If called from index page add query string to the action url
    // so that redirect goes to current folder
    if (current_dir) {
        let url = $('#fav-form').attr('action') + '?dir_id=' + current_dir;
        $('#fav-form').attr('action', url);
    }

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


function loadDatePicker() {
    // Attach an event handler to Date input box
    $("#modal").on("focus", "#id_next_update", function() {
        if (!$("#id_next_update").hasClass("active")) {
            // After the date picker is initialized prevent it from
            // un-initializing when focus changes
            $("#id_next_update").flatpickr();

            $("#id_next_update").click(function() {
                // Append the date picker to the modal to prevent focus stealing by modal
                let modal = document.getElementById("modal");
                let calendar = document.getElementsByClassName('flatpickr-calendar');
                modal.appendChild(calendar[calendar.length - 1]);
            })  
        }
    })
}