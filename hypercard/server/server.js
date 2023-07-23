const express = require('express');
const path = require('path');
const cors = require('cors');
const fs = require('fs');
const { Configuration, OpenAIApi } = require("openai");
const { type } = require('os');

const configuration = new Configuration({
  apiKey:"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",
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
        messages: [{ role: 'user', content: `You are hyperCardGPT and your tast is to return code and only code that will be injected into an html div tagged 'card'. You will receive the div as it currently is, and a command as to what to do. Your task it to just return the inner html implementing the command, and nothing else. Here is the inner html of the div now: ${div} and here is the command: ${command}` }],
      });
  
      console.log(completion.data.choices[0].message.content);
      return completion.data.choices[0].message.content;
    } catch (error) {
      console.error('Error creating chat completion:', error);
    }
  };


