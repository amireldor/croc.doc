'use strict';

const crocfarm = require('./crocfarm');

const docForm = document.getElementById('doc-form');
const docText = document.getElementById('doc-text');
const crocLine = document.getElementById('croc-line');
const feedButton = document.getElementById('feed-button');

docForm.addEventListener('submit', function (e) {
    e.preventDefault();

    disableFeeder();
    const doc = docText.value;
    crocfarm.feedCroc(doc).then(function (response) {
        enableFeeder();
        return response.json();
    }).then(function (json) {
        if (json.status == 'ok') {
            updateCrocLine(json);
        } else {
            displayError(json);
        }
    }).catch(function (error){
        enableFeeder();
        console.error(error);
    });
});

function disableFeeder() {
    feedButton.disabled = 'disabled';
}

function enableFeeder() {
    feedButton.disabled = '';
}

function updateCrocLine(json) {
    const name = crocLine.querySelector('.name');
    const link = crocLine.querySelector('.link');
    const docName = json.name || '';
    name.innerHTML = docName;
    link.href = location.protocol + '//' + location.host + '/' + docName;
}

function displayError(json) {
    console.log('error');
}
