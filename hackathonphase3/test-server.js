const http = require('http');

// Test if the server is responding
const options = {
  hostname: 'localhost',
  port: 3003,
  path: '/',
  method: 'GET',
  timeout: 5000 // 5 seconds timeout
};

console.log('Testing connection to http://localhost:3003');

const req = http.request(options, (res) => {
  console.log(`STATUS: ${res.statusCode}`);
  console.log(`HEADERS: ${JSON.stringify(res.headers)}`);

  res.setEncoding('utf8');
  res.on('data', (chunk) => {
    console.log(`BODY START: ${chunk.substring(0, 200)}...`);
  });

  res.on('end', () => {
    console.log('Response ended');
  });
});

req.on('error', (e) => {
  console.error(`Problem with request: ${e.message}`);
});

req.on('timeout', () => {
  console.log('Request timed out');
  req.destroy();
});

req.end();