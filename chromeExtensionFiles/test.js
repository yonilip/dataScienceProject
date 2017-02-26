/**
 * Created by dkutner on 25/02/2017.
 */


var xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        alert('Finished downloading ' + document.title);
    } else if (xmlhttp.readyState == 4) {
        alert('Something went wrong: ' + xmlhttp.status);
    }
};

xmlhttp.open('GET', 'https://127.0.0.1:8080/hello', true);
xmlhttp.send(null);