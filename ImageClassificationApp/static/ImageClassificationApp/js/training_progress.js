$(document).ready(function(){

    $(".hamburger .hamburger__inner").click(function(){
      $(".wrapper").toggleClass("active")
    })

    $(".top_navbar .fas").click(function(){
       $(".profile_dd").toggleClass("active");
    });

    $(".training-progress").addClass("active")


    var endpoint = '/api/data/training/history/'
    var val_acc = []


    $.ajax({
        method:'GET',
        url:endpoint,
        success:function(data){
            val_acc = data.val_accuracy
            val_loss = data.val_loss
            var epochs = Array.from(Array(val_acc.length), (_, i) => i + 1)
            console.log(val_acc)
            plot_data(epochs, val_acc, 'val-accuracy', 'Validation accuracy')
            plot_data(epochs, val_loss, 'val-loss', 'Validation loss')
        },
        error:function(error){
            console.log('error')
            console.log(error)
        }
    })

    function plot_data(x, y, canvas_id, title){
        var ctx = document.getElementById(canvas_id);
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: x,
                datasets: [{
                    label: title,
                    data: y,
                    borderWidth: 2,
                    fill: false,
                    borderColor: 'rgb(255, 99, 132)',
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }],
                    xAxes: [{
                      scaleLabel: {
                        display: true,
                        labelString: 'epochs'
                      }
                    }]
                }
            }
        });

    }

});






