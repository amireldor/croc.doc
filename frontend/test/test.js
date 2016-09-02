const demand = require('must');
const crocfarm = require('../js/crocfarm');

describe('Documents and stuff',  function () {
    describe('Posting new documents',  function () {

        beforeEach(function () {
            if (window.__html__) {
                document.body.innerHTML = window.__html__['test/index.html'];
            }
        });

        afterEach(function () {
            window.fetch.restore();
        });

        it('must parse the json from the backend', sinon.test(function (done) {
            // Stub a good response
            sinon.stub(window, 'fetch');
            const response = new window.Response('{"status": "ok", "name": "boarish-mosquito"}', {
                status: 200,
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            window.fetch.returns(Promise.resolve(response));

            crocfarm.feedCroc('I like chinese').then(function (result) {
                return result.json();
            }).then(function (json) {
                demand(json.status).not.undefined();
                demand(json.name).not.undefined();
                done();
            }).catch(function (error) {
                done(error);
            });
        }));
    });
});
