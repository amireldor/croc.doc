const demand = require('must');
const crocfarm = require('../js/crocfarm');

describe('Array',  function () {
    describe('#indexOf()',  function () {
        it('Should return -1 when value is not present',  function () {
            demand([1, 2, 3].indexOf(4)).equal(-1);
        });
    });
});

describe('Documents and stuff',  function () {
    describe('Posting new documents',  function () {

        beforeEach(function () {
            if (window.__html__) {
                document.body.innerHTML = window.__html__['test/index.html'];
            }

            sinon.stub(window, 'fetch');
            let response = new window.Response('{"status": "ok", "name": "boarish-mosquito"}', {
                status: 200,
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            window.fetch.returns(Promise.resolve(response));

        });

        afterEach(function () {
            window.fetch.restore();
        });

        it('must parse the json from the backend', sinon.test(function (done) {
            demand(document.getElementById('doc-text')).must.not.be.undefined();
            crocfarm.feedCroc('tasty deer').then(function (result) {
                return result.json();
            }).then(function (json) {
                demand(json.status).not.undefined();
                demand(json.name).not.undefined();
                //demand(json.dog).not.undefined();
                done();
            }).catch(function (error) {
                done(error);
            });
        }));

        it('must fail nicely if server doesn\'t like it', sinon.test(function () {
        }));
    });
});
