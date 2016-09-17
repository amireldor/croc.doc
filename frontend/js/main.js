'use strict';

const htmlentities = require('he');
const crocfarm = require('./crocfarm');
const docForm = document.getElementById('doc-form');

// Runs at application start
if (window.meta) {
    if (window.meta.all_is_nice) {
        showCrocLine();
    } else {
        const badName = window.meta.name || 'America';
        showError('Can\'t find "' + badName + '" inside the croc.<br>Maybe it\'s already out of the other hole...');
    }
}

docForm.addEventListener('submit', function (e) {
    e.preventDefault();
    hideError();
    disableFeeder();
    const docText = document.getElementById('doc-text');
    const doc = docText.value;
    crocfarm.feedCroc(doc).then(function (response) {
        enableFeeder();
        return response.json();
    }).then(function (json) {
        if (json.status == 'ok') {
            updateCrocLine(json.name);
            showCrocLine();
        } else {
            showError('Something\'s wrong with feeding the croc, maybe it\'s not hungry anymore...');
        }
    }).catch(function (error){
        enableFeeder();
        showError('Seems like the croc is not in the zoo anymore. Nothing to see, sorry.');
    });
});

function disableFeeder() {
    const feedButton = document.getElementById('feed-button');
    feedButton.disabled = 'disabled';
}

function enableFeeder() {
    const feedButton = document.getElementById('feed-button');
    feedButton.disabled = '';
}

function updateCrocLine(docName) {
    const crocLine = document.getElementById('croc-line');
    const name = crocLine.querySelector('.name');
    const link = crocLine.querySelector('.link');
    name.innerHTML = docName;
    link.href = location.protocol + '//' + location.host + '/' + docName;
}

function showCrocLine() {
    const crocLine = document.getElementById('croc-line');
    // Only add 'show' if it's not already there
    const classes = crocLine.className.split(' ');
    if (classes.indexOf('show') === -1) {
        if (crocLine.className.length >= 1) {
         crocLine.className += ' ';  // Pad in case of previous classes
        }
        crocLine.className += 'show';
    }
}

function showError(message) {
    const crocError = document.getElementById('error');
    crocError.innerHTML = htmlentities.encode(message);
    crocError.className = 'show';
}

function hideError() {
    const crocError = document.getElementById('error');
    crocError.className = '';
}
