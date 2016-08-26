let expect = chai.expect;
const crocfarm = require('../js/crocfarm');

describe('Array',  function () {
    describe('#indexOf()',  function () {
        it('Should return -1 when value is not present',  function () {
            expect([1, 2, 3].indexOf(4)).equal(-1);
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

        it('should parse the json from the backend', sinon.test(function () {
            expect(document.getElementById('doc-text')).is.not.undefined;
            return crocfarm.feedCroc('tasty deer').then(function (result) {
                return result.json();
            }).then(function (json) {
                // console.log('RESULT', json);
            });
        }));

        it('should fail nicely if server doesn\'t like it', sinon.test(function () {
        }));
    });
});
