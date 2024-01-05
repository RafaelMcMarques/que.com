// fetch qrcode and open popup
function openPopUp() {
    var googleChartApi = "https://chart.googleapis.com/chart?cht=qr&chs=200x200&chl=";
    var queueID = document.getElementById("queue-id").innerHTML;
    var queueName = document.getElementById("name").value;
    var queueURL = document.location.origin + "/join?id=" + queueID + "&name=" + queueName;
    var QRCodeURL = googleChartApi + encodeURIComponent(queueURL);
    document.getElementById("qrcode").src = QRCodeURL;
    document.getElementById("popup").style.display = "flex";
}

// close popup
function closePopUp() {
    document.getElementById("popup").style.display = "none";
}



