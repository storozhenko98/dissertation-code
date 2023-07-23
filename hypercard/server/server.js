const express = require('express');
const path = require('path');
const cors = require('cors');
const fs = require('fs');
const { Configuration, OpenAIApi } = require("openai");
const { type } = require('os');

const configuration = new Configuration({
  /*API Key*/
});
const openai = new OpenAIApi(configuration);

const app = express();
app.use(express.json());

// Middleware to set the "Content-Type" header for JavaScript modules


// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, 'public')));

const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Server is listening on port ${port}`);
});

app.post('/api', cors(), async (req, res) => {
    //make an object with the json data
    console.log(req.body);
    const data = req.body;
    //get the div and command from the object
    const div = data.div;
    const command = data.command;
    //get the completion from the gpt-4 model
    const completion = await getCompletion(div, command);
    //send the completion back to the client
    res.send(completion);
});


async function getCompletion(div, command) {
    try {
      const completion = await openai.createChatCompletion({
        model: 'gpt-4',
        temperature: 0.5,
        messages: [{ role: 'user', content: `
You are HyperCardGPT, an AI designed to generate HTML code that is injected into a specific HTML structure. Your task involves creating content that will fit within an inner div, tagged as 'inner-card', nested inside an outer div, tagged as 'card'. Always ensure that the content is returned within the tags <div id="inner-card"></div>.

Remember, under no circumstances should you alter the height, width, or any other properties of the inner div that might affect the outer div. Maintain the dimensions of the inner div and make it vertically scrollable if needed, ensuring it is always fully enclosed by the outer div.

You will receive the current state of the div and a command to implement. Respond with the updated inner HTML that fulfills the command—no explanations, no markdown, just pure HTML and inline CSS. Make certain that any element you add has a unique tag, avoiding repetition.

Here's your current div: ${div} and your command: ${command}. Follow all instructions diligently.` }],
      });
  
      console.log(completion.data.choices[0].message.content);
      return completion.data.choices[0].message.content;
    } catch (error) {
      console.error('Error creating chat completion:', error);
    }
  };

app.post('/publish', cors(), (req, res) => {
  const data = req.body;
  const html = data.html;
  const title = data.title;
  const author = data.author;
  const filename = `./public/cards/${title}_${author}.html`;
  fs.writeFile(filename, html, function(err) {
    if (err) {
      console.error(err);
      res.status(500).send('Error writing file');
    } else {
      res.send('File saved');
    }
  });
});

app.get('/cards', cors(), (req, res) => {
  const cards = [];
  fs.readdir('./public/cards', (err, files) => {
    if (err) {
      console.error(err);
      res.status(500).send('Error reading directory');
    } else {
      files.forEach(file => {
        const parts = file.split('_');
        if (parts.length === 2) {
          const card = {
            title: parts[0],
            author: parts[1].split('.')[0],
            link: `/cards/${file}`
          };
          cards.push(card);
        }
      });
      res.send(cards);
    }
  });
});
