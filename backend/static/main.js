'use strict';
(() => {
    // Override default form submit behavior
    const form = document.getElementById('doc-form');
    form.addEventListener('submit', e => {
        e.preventDefault();

        const doc = document.getElementById('doc-content').value;
        console.log('doc', doc);

        // Send the request for a new document
        const headers = {
            'content-type': 'application/json'
        };
        const body = {
            'doc': doc
        };
        fetch('/feedcroc', {headers, method:'POST', body: JSON.stringify(body)}).then(response => {
            console.log('hooray!', response.ok);
            if (!response.ok) {
                throw new Error("croc's said something is not ok with our request. Response is not ok.");
            }
            return response.json();
        }).then(json => {
            console.log('json', json);
        }).catch(error => {
            console.error('Something wrong happened', error);
        });
    });
})();
