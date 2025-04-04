const express = require('express');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const app = express();

const cors = require('cors');
app.use(cors());

app.use(express.json());
app.use(express.static(__dirname));

app.post('/reload', (req, res) => {
    exec('rm -rf output.txt && touch output.txt');
});

app.post('/update-python', (req, res) => {
    const usi = req.body.input;
    const usiFP = path.join(__dirname, 'user_input.txt');
    const opFP = path.join(__dirname, 'output.txt');

    fs.writeFile(usiFP, usi, (writeErr) => {
        exec('python3 main.py');
    });
});

app.get('/output', (req, res) => {
    const opFP = path.join(__dirname, 'output.txt');
    fs.readFile(opFP, 'utf8', (readErr, data) => {
        if (readErr) {
            res.status(500).send('couldnt read output.txt');
        } else {
            res.send(data);
        }
    });
});

const PORT = 3000;
app.listen(PORT, '0.0.0.0', () => {
    console.log(`http://0.0.0.0:${PORT}`);
});
