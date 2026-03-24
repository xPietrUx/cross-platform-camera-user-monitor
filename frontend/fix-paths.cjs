const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, 'build', 'index.html');
let html = fs.readFileSync(indexPath, 'utf8');

// Zamień wszystkie ścieżki absolutne na względne
html = html.replace(/href="\/_app/g, 'href="./_app');
html = html.replace(/src="\/_app/g, 'src="./_app');
html = html.replace(/import\("\/_app/g, 'import("./_app');

fs.writeFileSync(indexPath, html);
console.log('✅ Ścieżki w index.html zostały naprawione!');
