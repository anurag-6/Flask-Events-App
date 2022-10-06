setInterval(time,1000);

function time(){
    var d = new Date();
    lt =d.toLocaleString()
    document.getElementById('livetime').innerHTML = lt;
    
}

