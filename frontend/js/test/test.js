let assert = require('assert');

describe('Array', function() {
    describe('#indexOf()', function() {
        it('Should return -1 when value is not present', function() {
            assert.equal(-1, [1, 2, 3].indexOf(4));
        });
    });
});
