$(document).ready(function(){

    $(".hamburger .hamburger__inner").click(function(){
      $(".wrapper").toggleClass("active")
    })

    $(".top_navbar .fas").click(function(){
       $(".profile_dd").toggleClass("active");
    });

    $(".new_task").toggleClass("active")

    $('label[for="id_imageclass_set-0-DELETE"]').hide();

    $('label[for="id_task_set-0-DELETE"]').hide();

    $("#id_task_set-0-DELETE").hide()
    $("#submit-id-submit").removeClass("btn")
    $("#submit-id-submit").removeClass("btn-primary")

});