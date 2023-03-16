function sendJSON(){
    let result = document.querySelector('.result');
    let region = document.querySelector('#id_region');
    let adults = document.querySelector('#id_adults');
    let children = document.querySelector('#id_children');
    let infants = document.querySelector('#id_infants');
    let start = document.querySelector('#id_start');
    let end = document.querySelector('#id_end');

    // Creating a XHR object
    let xhr = new XMLHttpRequest();
    console.log("testing");
    console.log(endpoint);
    let url = endpoint;

    // open a connection
    xhr.open("POST", url, true);

    // Set the request header i.e. which type of content you are sending
    xhr.setRequestHeader("Content-Type", "application/json");

    // Create a state change callback
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {

            // Print received data from server
            result.innerHTML = this.responseText;

        }
    };

    // Converting JSON data to string
    var data = JSON.stringify({ "region": region.value,
    "adults": adults.value,
    "children": adults.children,
    "infants": adults.infants,
    "start": adults.start,
    "end": adults.end,
     });

    // Sending data with the request
    xhr.send(data);
}