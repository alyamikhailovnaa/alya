require('dotenv').config();
const fs = require('fs');
const path = require('path');

async function main() {
  const logDir = path.join(__dirname, '../logs');
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir);
  }

  const date = new Date().toISOString().split('T')[0];
  const logFile = path.join(logDir, `activity.md`);

  const content = `- Activity log for ${date}: System running normally.\n`;

  // Append to activity log
  fs.appendFileSync(logFile, content, 'utf8');

  console.log(`Activity log updated for ${date}`);
}

main().catch(console.error);
