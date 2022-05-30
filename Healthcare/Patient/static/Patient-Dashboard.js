window.onload = forfirst;

function forfirst(){
    document.getElementById("p-info").style.display = "block";
    document.getElementById("l-diagnosis").style.display = "none";
    document.getElementById("prescrips").style.display = "none";
    document.getElementById("btn1").style.backgroundColor = "white";
    document.getElementById("btn2").style.background = "none"
    document.getElementById("btn3").style.background = "none";
    document.getElementById("btn1").style.boxShadow = "0px 0px 2px rgba(0,0,0,0.5)";
    document.getElementById("btn2").style.boxShadow = "none";
    document.getElementById("btn3").style.boxShadow = "none";

    
}

function forsecond(){
    document.getElementById("p-info").style.display = "none";
    document.getElementById("l-diagnosis").style.display = "block";
    document.getElementById("prescrips").style.display = "none";
    document.getElementById("btn1").style.background = "none";
    document.getElementById("btn2").style.backgroundColor = "white";
    document.getElementById("btn3").style.background = "none";
    document.getElementById("btn1").style.boxShadow = "none";
    document.getElementById("btn2").style.boxShadow = "0px 0px 2px rgba(0,0,0,0.5)";
    document.getElementById("btn3").style.boxShadow = "none";
}

function forthird(){
    document.getElementById("p-info").style.display = "none";
    document.getElementById("l-diagnosis").style.display = "none";
    document.getElementById("prescrips").style.display = "block";
    document.getElementById("btn1").style.background = "none";
    document.getElementById("btn2").style.background = "none";
    document.getElementById("btn3").style.backgroundColor = "white";
    document.getElementById("btn1").style.boxShadow = "none";
    document.getElementById("btn2").style.boxShadow = "none";
    document.getElementById("btn3").style.boxShadow = "0px 0px 2px rgba(0,0,0,0.5)";
}