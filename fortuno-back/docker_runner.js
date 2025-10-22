const { spawn } = require('child_process');

const args = process.argv.slice(2);
const child = spawn('docker-compose', args, { stdio: 'inherit' });

child.on('close', (code) => {
    process.exit(code);
});