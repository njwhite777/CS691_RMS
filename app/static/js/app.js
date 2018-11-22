function save(id,type,url,del_id){

  console.log(id);
  console.log($(id).serialize());

  var onSuccess = function(){
    console.log(id);
    switch(type){
      case "put":
        console.log("Updated fields for " + id);
        break;
      case "post":
        console.log("POSTED fields for " + id);
        clearRestaurantFields(id);
        break;
      case "delete":
        $(del_id).css("display","none");
        break;
    }
  };

  console.log($(id).serialize());

  var onFailure = function(){
    console.log("SOMETHING WENT WRONG.");
  };

  $.ajax({
    url: url,
    type: type,
    data: $(id).serialize(),
    success: onSuccess,
    error: onFailure
  });
}


function setupCheckedEmployees(){
  console.log("HERE!!!");
}

function clearFields(id){
  $(id).trigger('reset');
  $(id).find("select").selectpicker('refresh');
}
