'use strict';

const crocfarm = require('./crocfarm');

const docForm = document.getElementById('doc-form');
const docText = document.getElementById('doc-text');
const crocLine = document.getElementById('croc-line');

docForm.addEventListener('submit', function (e) {
    e.preventDefault();
    console.log('WeeE', docText.value);

    const request = {
        doc: docText.value
    };
    const headers = {
        'Content-Type': 'application/json'
    };

    crocfarm.feedCroc(doc).then(function (response) {
        return response.json();
    }).then(function (json) {
        // Show NICE stuff in the GUI
        if (json.status == 'ok') {
            updateCrocLine(json);
        } else {
            displayError(json);
        }
    }).catch(function (error){
        // Show BAD stuff in the GUI
        console.error(error);
    });

});

function updateCrocLine(json) {
    const name = crocLine.querySelector('.name');
    const link = crocLine.querySelector('.link');
    const docName = json.name || '';
    name.innerHTML = docName;
    link.href = location.protocol + '//' + location.host + '/' + docName;
}

function displayError(json) {
    console.log('erorr');
}
