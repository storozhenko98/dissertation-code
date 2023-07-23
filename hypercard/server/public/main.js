let targetElement = null; // Variable to store the clicked element

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
    document.getElementById('command').value = 'Regarding ' + event.target.id + ': ';
});

// Event listener for clicks on any child of the card div
document.getElementById('card').addEventListener('click', function(event) {
    if (event.target.id !== 'card') { // Ignore clicks on the card itself
        targetElement = event.target; // Store the clicked element
        let modal = document.getElementById('modal');
        modal.style.display = 'block'; // Show the modal
        document.getElementById('modal-text').value = targetElement.textContent; // Populate the text input with the current text
    }
});

// Event listener for the Save button in the modal
document.getElementById('modal-save').addEventListener('click', function() {
    if (targetElement) { // If an element was clicked
        targetElement.textContent = document.getElementById('modal-text').value; // Update the text
        targetElement.style.color = document.getElementById('modal-color').value; // Update the color
    }
    document.getElementById('modal').style.display = 'none'; // Hide the modal
});


//publish to server 
document.getElementById('publish').addEventListener('click', function() {
    const title = prompt("Enter a title for your card: ");
    const author = prompt("Enter your name: ");
    let cardHtml = document.getElementById('card').outerHTML;
    let blob = new Blob([cardHtml], {type: 'text/html'});
    let url = URL.createObjectURL(blob);
    let link = document.createElement('a');
    link.href = url;
    link.download = `${title}_${author}.html`;
    link.click();
    //publish to server
    fetch('/publish', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            html: cardHtml,
            title: title,
            author: author
        })
    })
    .then(response => response.text())
    .then(text => {
        // do something with the response...
        console.log(text);
    })
    .catch(error => console.error(error));
}
);

// Event listener for the browse button to go to cards home html
document.getElementById('browse').addEventListener('click', function() {
    window.location.href = './cards/home.html';
}
);

//event listener for div clear
document.getElementById('clear').addEventListener('click', function() {
    document.getElementById('inner-card').innerHTML = '';
}
);

//modal cancel 
document.getElementById('modal-cancel').addEventListener('click', function() {
    document.getElementById('modal').style.display = 'none';
}
);