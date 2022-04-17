/*function getmundiLayer(){
    $.ajax({
        url: "mundiLayer",
        method: "GET",
        //contentType: 'application/json',
        success: function (returned_data){
            data = JSON.parse(returned_data)
            alert(data);
        },
        error: function () {
            alert('An error occured');
        }
    })
}*/

function getmundiLayer(){
    $.get('mundiLayer', function (data) {
        console.log(JSON.parse(data));
        prueba(data);
    })
}

/* let ctx = document.getElementById("myChart").getContext("2d");
let myChart = new Chart(ctx, {
    type:"bar",
    data:{
        labels:['Col1','Col2','Col3'],
        dataset:[{
            label: 'Num datos',
            data:[10,12,8]
        }]
    }
}); */
