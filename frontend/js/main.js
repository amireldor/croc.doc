'use strict';

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

    fetch('/feedcroc', {method: 'POST', headers, body: JSON.stringify(request)}).then(response => {
        if (!response.ok) {
            throw new Error('Response does not have an ok status');
        }
        return response.json();
    }).then(json => {
        console.log('kson', json);
    }).catch(() => {
        console.error('Some error with the request :(');
    });;
});
