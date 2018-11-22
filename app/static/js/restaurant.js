function saveRestaurant(id,type,url,del_id){

  console.log($(id).serialize());
  var onSuccess = function(){
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

function clearRestaurantFields(id){
  $(id).trigger('reset');
  $(id).find("select").selectpicker('refresh');
}
