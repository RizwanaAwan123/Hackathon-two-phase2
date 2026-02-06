const http = require('http');

// Simple test to check if the page loads
const options = {
  hostname: 'localhost',
  port: 3004,
  path: '/',
  method: 'GET',
  headers: {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
  }
};

const req = http.request(options, (res) => {
  console.log(`Status: ${res.statusCode}`);
  console.log('Headers:', res.headers);

  res.on('data', (chunk) => {
    console.log('Received chunk:', chunk.toString().substring(0, 200) + '...');
  });

  res.on('end', () => {
    console.log('Response ended');
  });
});

req.on('error', (e) => {
  console.error('Request error:', e.message);
});

req.end();