// Function to handle the command
function handleCommand() {
    let command = document.getElementById('command');
    let divContents = document.getElementById('card').innerHTML;

    fetch('/api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            div: divContents,
            command: command.value
        })
    })
    .then(response => response.text())
    .then(text => {
        // do something with the response...
        document.getElementById('card').innerHTML = text;
        console.log(text);
    })
    .catch(error => console.error(error));

    // Add the command to the history
    let li = document.createElement('li');
    li.textContent = command.value;
    document.getElementById('history').appendChild(li);

    // Clear the command input
    command.value = '';
}

// Event listener for the submit button
document.getElementById('submit').addEventListener('click', handleCommand);

// Event listener for the Enter key in the text box
document.getElementById('command').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevents the default action (form submission)
        handleCommand();
    }
});

// Event listener for clicks in the card div
document.getElementById('card').addEventListener('click', function(event) {
    document.getElementById('command').value = 'Regarding ' + event.target.tagName.toLowerCase() + ': ';
});
