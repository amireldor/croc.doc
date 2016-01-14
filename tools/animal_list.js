var cheerio = require('cheerio');
var fs = require('fs');

var html = fs.readFileSync('./list-of-animals-wikipedia.html')
var $ = cheerio.load(html);

// will match one-word animals only
var re_select_animals = /([A-Z]\w+)/

var writer = fs.createWriteStream('./Animals.txt');
var items = 0;

$("tr td a[title!='']").each(function (index, animal) {
    var animal = $(animal).text().match(re_select_animals);
    if (animal === null) return;
    animal = animal[0];
    writer.write(animal + '\n');
    items++;
});

writer.end();
console.log('Wrote', items, 'items.');
