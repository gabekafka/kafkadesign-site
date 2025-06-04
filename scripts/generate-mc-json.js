//
// scripts/generate-mc-json.js
//
// Reads assets/data/mc-member-data.csv and writes a JSON file at js/mc-member-data.json.
// Run this whenever your MC CSV changes.
//

const fs = require('fs');
const path = require('path');

// 1) Path to the MC CSV
const csvPath = path.join(__dirname, '..', 'assets', 'data', 'mc-member-data.csv');

// 2) Read the CSV file
let csvContent;
try {
  csvContent = fs.readFileSync(csvPath, 'utf8').trim();
} catch (err) {
  console.error('❌ Error reading MC CSV at:', csvPath);
  console.error(err);
  process.exit(1);
}
if (!csvContent) {
  console.error('❌ MC CSV file is empty:', csvPath);
  process.exit(1);
}

// 3) Split into lines and parse the header row
const lines = csvContent.split('\n');
const headers = lines[0].split(',').map(h => h.trim());

// 4) Find the “NAME” column (or whatever your “identifier” column is called)
//    (If your MC CSV uses a different header name, adjust this accordingly.)
const nameIndex = headers.findIndex(h => h.toUpperCase() === 'NAME');
if (nameIndex < 0) {
  console.error('❌ Could not find a "NAME" column in MC CSV header.');
  console.error('    Found headers:', headers);
  process.exit(1);
}

// 5) Build an object whose keys are the NAME (uppercase, no spaces),
//    and whose values are objects mapping each column → that row’s value.
const resultObj = {};
for (let i = 1; i < lines.length; i++) {
  const row = lines[i].split(',').map(cell => cell.trim());
  const rawName = row[nameIndex];
  if (!rawName) continue; // skip empty rows
  const key = rawName.replace(/\s+/g, '').toUpperCase();
  resultObj[key] = {};
  headers.forEach((colName, j) => {
    resultObj[key][colName] = row[j] || '';
  });
}

// 6) Serialize to JSON (pretty-printed)
const jsonString = JSON.stringify(resultObj, null, 2);

// 7) Write out to js/mc-member-data.json
const outPath = path.join(__dirname, '..', 'js', 'mc-member-data.json');
try {
  fs.writeFileSync(outPath, jsonString, 'utf8');
  console.log('✅ Successfully wrote JSON to:', outPath);
} catch (err) {
  console.error('❌ Error writing MC JSON at:', outPath);
  console.error(err);
  process.exit(1);
}