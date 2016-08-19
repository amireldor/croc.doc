let expect = chai.expect;

describe('Array', function() {
    describe('#indexOf()', function() {
        it('Should return -1 when value is not present', function() {
            expect([1, 2, 3].indexOf(4)).equal(-1);
        });
    });
});

describe('Documents and stuff', function() {
    describe('Posting new documents', function() {

        beforeEach(function () {
            sinon.stub(window, 'fetch');
            let res = new window.Response('{"status": "ok", "name": "boarish-mosquito"}', {
                status: 200,
                headers: {
                    'Content-type': 'application/json'
                }
            });
            window.fetch.returns(Promise.resolve(res));
        });

        afterEach(function () {
            window.fetch.restore();
        });

        it('should parse the json from the backend', sinon.test(function () {
            return crocfarm.feedCroc('tasty deer');
        }));

        it('should fail nicely if server doesn\'t like it', sinon.test(function () {
        }));
    });
});
