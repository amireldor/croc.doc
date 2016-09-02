'use strict';

exports.feedCroc = function (doc) {
    const headers = new Headers({
        'content-type': 'application/json'
    });
    const body = JSON.stringify({doc});

    return fetch('/feedcroc', {method: 'POST', headers, body});
}
