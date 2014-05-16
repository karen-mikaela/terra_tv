$("#save").click(function(){
    var car = {
            model: new FormData($('#model')),
            year: new FormData($('#year')),
            manufacturer: new FormData($('#manufacturer')),
            photo: new FormData($('#photo')[0])
        }
  $.post("/admin/create/",car, function(data, status){
    console.log(data)
    console.log(status)
    if(status == "success"){
        console.log( "dssssss")
    }

  });
});