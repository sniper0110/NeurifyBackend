$(document).ready(function(){

    $(".hamburger .hamburger__inner").click(function(){
      $(".wrapper").toggleClass("active")
    })

    $(".top_navbar .fas").click(function(){
       $(".profile_dd").toggleClass("active");
    });

    $(".dashboard").addClass("active")

});