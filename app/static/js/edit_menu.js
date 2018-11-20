
original_text = {};

function makeEditable(menu_item){
  var menu_item_handle = document.getElementById("panel_item_"+menu_item);
  document.getElementById("save_button_"+menu_item).style.visibility = "visible";
  document.getElementById("discard_button_"+menu_item).style.visibility = "visible";
  document.getElementById("edit_button_"+menu_item).style.display = "none";

  var items = ["name_"+menu_item,"price_"+menu_item,"information_"+menu_item,"ingredients_"+menu_item,"allergy_information_"+menu_item];
  for(var i =0;i<items.length;i++){
    original_text[items[i]] = document.getElementById(items[i]).innerHTML;
    var editElement = document.getElementById(items[i]);
    editElement.contentEditable=true;
    editElement.className = "form-control";
  }
}

function discardEdits(menu_item){
  document.getElementById("save_button_"+menu_item).style.visibility = "hidden";
  document.getElementById("discard_button_"+menu_item).style.visibility = "hidden";
  document.getElementById("edit_button_"+menu_item).style.display = "block";

  var items = ["name_"+menu_item,"price_"+menu_item,"information_"+menu_item,"ingredients_"+menu_item,"allergy_information_"+menu_item];
  for(var i =0;i<items.length;i++){
    var editElement = document.getElementById(items[i]);
    editElement.innerHTML = original_text[items[i]];
    editElement.contentEditable=false;
    editElement.className = "";
  }
}

function saveEdits(menu_item){
  var xhr = new XMLHttpRequest();
  xhr.open("PUT","/menuItem", true);
  xhr.setRequestHeader('Content-Type', 'application/json');

  xhr.onreadystatechange = function(){
    if( xhr.readyState == 4 && xhr.status==200 ){
      console.log("Success!")
    }else{
      console.log("Something went wrong with post request.")
    }
  };

  var data = {};
  var items = ["id_"+menu_item,"name_"+menu_item,"price_"+menu_item,"information_"+menu_item,"ingredients_"+menu_item,"allergy_information_"+menu_item];

  for(var i =0;i<items.length;i++){
    var data_item = items[i].split("_").slice(0,-1).join("_");
    console.log(data_item)
    data[data_item]= document.getElementById(items[i]).innerHTML;
    document.getElementById(items[i]).className = "";
  }
  xhr.send(JSON.stringify(data));

  document.getElementById("save_button_"+menu_item).style.visibility = "hidden";
  document.getElementById("discard_button_"+menu_item).style.visibility = "hidden";
  document.getElementById("edit_button_"+menu_item).style.display = "block";
}

function addNewItem(){
  var add_items = ["add_name","add_price","add_information","add_allergy_information"];
  var data = {};

  for(var i =0;i<add_items.length;i++){
    var item = document.getElementById(add_items[i]);
    data[add_items[i].split("_").slice(1).join("_")] = item.innerHTML;
  }

  var xhr = new XMLHttpRequest();
  xhr.open("POST","/menuItem", true);
  xhr.setRequestHeader('Content-Type', 'application/json');

  xhr.onreadystatechange = function(){
    console.log(xhr);
    if( xhr.readyState == 4 && xhr.status==200 ){
      for(var i =0;i<add_items.length;i++){
        var item = document.getElementById(add_items[i]);
        item.innerHTML = "";
      }
    }else{
      console.log("Something went wrong with post request.")
    }
    location.reload();

  }
  xhr.send(JSON.stringify(data));

};
