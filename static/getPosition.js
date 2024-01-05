// updates page when user position changes
function getPosition() {
    fetch('/getPosition')
        .then(response => response.json())
        .then(data => {
            currPosition = data.position;
            if (typeof window.previousPosition !== 'undefined' && currPosition != window.previousPosition) {
                location.reload();
            }
            else {
                window.previousPosition = currPosition;
            }
        })
}

getPosition();
setInterval(getPosition, 5000);