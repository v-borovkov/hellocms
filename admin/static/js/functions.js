$(document).ready(function(){

  // Get the Sidenav
  var mySidenav = document.getElementById("mySidenav");

  // Get the DIV with overlay effect
  var overlayBg = document.getElementById("myOverlay");

  // Toggle between showing and hiding the sidenav, and add overlay effect
  function w3_open() {
      if (mySidenav.style.display === 'block') {
          mySidenav.style.display = 'none';
          overlayBg.style.display = "none";
      } else {
          mySidenav.style.display = 'block';
          overlayBg.style.display = "block";
      }
  }

  // Close the sidenav with the close button
  function w3_close() {
      console.log("test");
      mySidenav.style.display = "none";
      overlayBg.style.display = "none";
  }


 $('#content').trumbowyg();

 $( function() {
     $( "#sortable1, #sortable2" ).sortable({
       connectWith: ".connectedSortable"
     }).disableSelection();
   });

 var img = $('img#an-img');
$("#editor").trumbowyg("openModalInsert", {
    title: "A title for modal box",
    fields: {
        url: {
            value: img.attr('src')
        },
        alt: {
            label: 'Alt',
            name: 'alt',
            value: img.attr('alt')
        },
        example: {
            // Missing label is replaced by the key of this object (here 'example')
            // Missing name is the same
            // When value is missing, value = ''
        }
    },
    callback: function(values){
        img.attr('src', values['url']);
        img.attr('alt', values['alt']);

        return true; // Return true if you have finished with this modal box
        // If you do not return anything, you need manage yourself the closure of the modal box
    }
});

});
