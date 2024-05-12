let urllink = document.getElementById('urllink');
let shorten_url_div = document.getElementById('shorten_url');
let shortenurllink = document.getElementById('shortenurllink');


function fetch_short_url(){
    let longurllink = urllink.value;
    fetch(`http://127.0.0.1:5000/shorten_url?longurl=${longurllink}`)
    .then(response => response.text())
    .then(data => {
        let shorturl = "http://127.0.0.1:5000/" + String(data).slice(18,26);
        shorten_url_div.style.display = "block";
        shortenurllink.value = shorturl;
    })
    .catch(error => console.error('Error:', error));
}