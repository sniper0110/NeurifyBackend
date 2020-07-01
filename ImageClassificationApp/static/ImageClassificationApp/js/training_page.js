$(document).ready(function(){

    $(".hamburger .hamburger__inner").click(function(){
      $(".wrapper").toggleClass("active")
    })

    $(".top_navbar .fas").click(function(){
       $(".profile_dd").toggleClass("active");
    });

    $(".training").addClass("active")

    $('label[for="id_classificationdeeplearningmodel-0-DELETE"]').hide();
    $("#id_classificationdeeplearningmodel-0-DELETE").hide();
});




