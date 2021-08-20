$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    console.log("tab shown...");
    localStorage.setItem('activeTab', $(e.target).attr('href'));
});

// read hash from page load and change tab
var activeTab = localStorage.getItem('activeTab');
if(activeTab){
    $('.nav-tabs a[href="' + activeTab + '"]').tab('show');
}