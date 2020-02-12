const dialogue = document.getElementById('response');
const input = document.getElementById('textarea');
const sendMessage = document.getElementById('button');
let i = 1;
let map;
let elt;


function ajaxPost(body,callback){
  let request = new XMLHttpRequest();
  request.onreadystatechange = function() {
    if (this.readyState == XMLHttpRequest.DONE && this.status == 200) {
      let response = JSON.parse(this.responseText);
      setTimeout(callback,3000,response);
    }
  }
  request.open("POST", "https://thegrandpybot.herokuapp.com");
  request.setRequestHeader("Content-Type", "application/json");
  request.send(JSON.stringify(body));
};


function initMap(lat,lng) {
  let coord = {lat: lat, lng: lng};
  map = new google.maps.Map(document.getElementById('map'+ i), {
    center: coord,
    zoom: 16
  });
  let marker = new google.maps.Marker({position: coord, map: map});
};


function addElt(){
  let newElt = document.createElement('div');
  newElt.classList.add('col-md-12');
  dialogue.appendChild(newElt);
  lastMessage();
  return newElt
};


function lastMessage(){
  let lastMessage = dialogue.lastChild;
  lastMessage.scrollIntoView()
};


function insertResponse(response){
  elt.classList.replace('loader','custom')
  elt.classList.add('borderpy');
  if (typeof response.data == 'string') {
    elt.innerHTML = '<p>'+response.data+'</p>';
  }else{
    elt.innerHTML = '<div id="map'+i+'"></div><p>'+
    response.data[2]+'</br>'+response.data[1]+'</p>';

    initMap(response.data[0].lat, response.data[0].lng);
    i += 1;
  }
  lastMessage();
}

function userPost(){
  elt = addElt();
  elt.classList.add('custom', 'borderuser');
  elt.innerHTML = '<p>' + input.value + '</p>';
}

function grandPyPost(){
  elt = addElt();
  elt.classList.add('loader');
  body = {'message': input.value}
  ajaxPost(body, insertResponse);
}


function discussion(e){
  e.preventDefault();
  if (input.value.length > 0) {
    userPost();
    grandPyPost();
    input.value = '';
  }
};


input.addEventListener('keydown', function(e){
  if (e.key === 'Enter') {
      discussion(e);
  }
});

sendMessage.addEventListener('click',function(e){
  discussion(e);
});
