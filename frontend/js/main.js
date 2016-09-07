'use strict';

const crocfarm = require('./crocfarm');

const docForm = document.getElementById('doc-form');
const docText = document.getElementById('doc-text');
const crocLine = document.getElementById('croc-line');
const feedButton = document.getElementById('feed-button');

if (window.meta && window.meta.all_is_nice) {
    updateCrocLine(window.meta.name || 'you-should-not-see-this');
    showCrocLine();
}

docForm.addEventListener('submit', function (e) {
    e.preventDefault();

    disableFeeder();
    const doc = docText.value;
    crocfarm.feedCroc(doc).then(function (response) {
        enableFeeder();
        return response.json();
    }).then(function (json) {
        if (json.status == 'ok') {
            updateCrocLine(json.name);
            showCrocLine();
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

function updateCrocLine(docName) {
    const name = crocLine.querySelector('.name');
    const link = crocLine.querySelector('.link');
    name.innerHTML = docName;
    link.href = location.protocol + '//' + location.host + '/' + docName;
}

function showCrocLine() {
    // Only add 'show' if it's not already there
    const classes = crocLine.className.split(' ');
    if (classes.indexOf('show') === -1) {
        if (crocLine.className.length >= 1) {
         crocLine.className += ' ';  // Pad in case of previous classes
        }
        crocLine.className += 'show';
    }
}

function displayError(json) {
    console.log('error');
}
