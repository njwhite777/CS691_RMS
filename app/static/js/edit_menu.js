
original_text = {};

function makeEditable(menu_item){
  var menu_item_handle = document.getElementById("panel_item_"+menu_item);
  document.getElementById("save_button_"+menu_item).style.visibility = "visible";
  document.getElementById("discard_button_"+menu_item).style.visibility = "visible";
  document.getElementById("edit_button_"+menu_item).style.display = "none";
  var items = ["name_"+menu_item,"price_"+menu_item,"information_"+menu_item,"allergens_"+menu_item];
  for(var i =0;i<items.length;i++){

    original_text[items[i]] = document.getElementById(items[i]).innerHTML;
    document.getElementById(items[i]).contentEditable=true;
  }
}

function discardEdits(menu_item){
  document.getElementById("save_button_"+menu_item).style.visibility = "hidden";
  document.getElementById("discard_button_"+menu_item).style.visibility = "hidden";
  document.getElementById("edit_button_"+menu_item).style.display = "block";

  var items = ["name_"+menu_item,"price_"+menu_item,"information_"+menu_item,"allergens_"+menu_item];
  for(var i =0;i<items.length;i++){
    document.getElementById(items[i]).innerHTML = original_text[items[i]];
    document.getElementById(items[i]).contentEditable=false;
  }
}

function saveEdits(menu_item){
  
}
