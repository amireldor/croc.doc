'use strict';

const crocfarm = require('./crocfarm');

const docForm = document.getElementById('doc-form');
const docText = document.getElementById('doc-text')

docForm.addEventListener('submit', function (e) {
    e.preventDefault();
    console.log('WeeE', docText.value);

    const request = {
        doc: docText.value
    };
    const headers = {
        'Content-Type': 'application/json'
    };

    console.log(crocfarm);
    crocfarm.feedCroc(doc).then(function (json) {
        // Show NICE stuff in the GUI
        console.log(success, json);
    }).catch(function (error){
        // Show BAD stuff in the GUI
        console.error(error);
    });

    //fetch('/feedcroc', {method: 'POST', headers, body: JSON.stringify(request)}).then(response => {
    //    if (!response.ok) {
    //        throw new Error('Response does not have an ok status');
    //    }
    //    return response.json();
    //}).then(json => {
    //    console.log('kson', json);
    //}).catch(() => {
    //    console.error('Some error with the request :(');
    //});;
});
