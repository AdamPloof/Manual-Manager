// Append the page query string to the current search url
let page_btns = document.getElementsByClassName('page-nav');

for (let i = 0; i < page_btns.length; i++) {
    let url = new URL(window.location.href);
    let query_string = url.search;
    let search_params = new URLSearchParams(query_string);
    let page_num = page_btns[i].dataset.page;
    
    if (search_params.has('page')) {
        search_params.set('page', page_num);
    }
    else {
        search_params.append('page', page_num);
    }    

    url.search = search_params.toString();
    page_btns[i].href = url.toString();
}