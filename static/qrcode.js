// fetch qrcode and open popup
function openPopUp() {
    var googleChartApi = "https://chart.googleapis.com/chart?cht=qr&chs=200x200&chl=";
    var queueID = document.getElementById("queue-id").innerHTML;
    var queueURL = document.location.origin + "/join?id=" + queueID;
    var QRCodeURL = googleChartApi + queueURL;
    document.getElementById("qrcode").src = QRCodeURL;
    document.getElementById("popup").style.display = "flex";
}

// close popup
function closePopUp() {
    document.getElementById("popup").style.display = "none";
}



