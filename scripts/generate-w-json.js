//
// scripts/generate-w-json.js
//
// Reads assets/data/w-member-data.csv and writes a JSON file at js/w-member-data.json.
// You can re-run this script whenever the CSV changes.
//

const fs = require('fs');
const path = require('path');

// 1) Build the path to your CSV file
const csvPath = path.join(__dirname, '..', 'assets', 'data', 'w-member-data.csv');

// 2) Read the CSV file contents (UTF-8 text)
let csvContent;
try {
  csvContent = fs.readFileSync(csvPath, 'utf8').trim();
} catch (err) {
  console.error('❌ Error reading CSV at:', csvPath);
  console.error(err);
  process.exit(1);
}
if (!csvContent) {
  console.error('❌ CSV file is empty:', csvPath);
  process.exit(1);
}

// 3) Split lines and parse header
const lines = csvContent.split('\n');
const headers = lines[0].split(',').map(h => h.trim());

// Find the “NAME” column index (case-insensitive)
const nameIndex = headers.findIndex(h => h.toUpperCase() === 'NAME');
if (nameIndex < 0) {
  console.error('❌ Could not find a "NAME" column in CSV header.');
  console.error('    Found headers:', headers);
  process.exit(1);
}

// 4) Build a JavaScript object where each key is the NAME (uppercase, no spaces)
//    and each value is an object mapping each column name to that row’s value.
const resultObj = {};
for (let i = 1; i < lines.length; i++) {
  const row = lines[i].split(',').map(cell => cell.trim());
  const rawName = row[nameIndex];
  if (!rawName) continue; // skip blank lines or rows without a NAME
  const key = rawName.replace(/\s+/g, '').toUpperCase(); 
  resultObj[key] = {};
  headers.forEach((colName, j) => {
    resultObj[key][colName] = row[j] || ''; 
  });
}

// 5) Serialize that object to JSON (pretty-printed)
const jsonString = JSON.stringify(resultObj, null, 2);

// 6) Write the JSON out to js/w-member-data.json
const outPath = path.join(__dirname, '..', 'js', 'w-member-data.json');
try {
  fs.writeFileSync(outPath, jsonString, 'utf8');
  console.log('✅ Successfully wrote JSON to:', outPath);
} catch (err) {
  console.error('❌ Error writing JSON at:', outPath);
  console.error(err);
  process.exit(1);
}