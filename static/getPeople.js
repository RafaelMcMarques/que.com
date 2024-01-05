// updates page when number of people in queue changes
function getPeople() {
    fetch('/getPeople')
        .then(response => response.json())
        .then(data => {
            currNumber = data.number;
            if (typeof window.previousNumber !== 'undefined' && currNumber !== window.previousNumber) {
                location.reload();
            }
            else {
                window.previousNumber = currNumber;
            }
        })
}

getPeople();
setInterval(getPeople, 5000);