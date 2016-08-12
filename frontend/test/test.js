let expect = chai.expect;

describe('Array', function() {
    describe('#indexOf()', function() {
        it('Should return -1 when value is not present', function() {
            expect([1, 2, 3].indexOf(4)).equal(-1);
        });
    });
});
