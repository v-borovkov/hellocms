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

  /*widgets*/
  $("#banner").click(function(){
      console.log("banner");
      color ="w3-cyan";
      value = '<div id="widget"><header class="w3-container test w3-cyan w3-text-white w3-center w3-padding-128"><h1 class="w3-margin w3-jumbo">Welcome to HelloCMS v0.4</h1><p class="w3-xlarge">Template by w3.css</p><input type="button" class="w3-button w3-cyan w3-border w3-border-white w3-text-white w3-hover-white w3-hover-text-cyan w3-padding-large w3-large w3-margin-top" value="Get Started"  style="background-color:[[backgroundcolor]]"></header></div>';
      $("ul").append("<li>" + value + "<input type='hidden' name='widgets' class='w3-input w3-border' value='" + value + "'></li>");
  });

  $("#text").click(function(){
      console.log("text");
      $("ul").append("<li><textarea id='textwidget' class='w3-input' name='widgets' rows='16'></textarea></li>");
      $('#textwidget').trumbowyg();
  });
  //$("ul").append("<li><input type='hidden' name='widgets' class='w3-input w3-border' value=''></li>");

   $('#content').trumbowyg();


  // Close the sidenav with the close button
  function w3_close() {
      console.log("test");
      mySidenav.style.display = "none";
      overlayBg.style.display = "none";
  }

  var editor = ace.edit("editor");
  editor.setTheme("ace/theme/monokai");
  editor.getSession().setMode("ace/mode/html");

  var input = $('textarea#area');
  editor.getSession().on("change", function () {
      input.val(editor.getSession().getValue());
  });



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
