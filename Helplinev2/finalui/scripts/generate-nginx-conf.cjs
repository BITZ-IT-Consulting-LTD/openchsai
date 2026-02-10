/**
 * Generates nginx.conf from the taxonomy contract based on VITE_DEFAULT_COUNTRY.
 * Runs during Docker build so nginx proxies match the selected environment.
 */
const fs = require('fs');
const path = require('path');

const country = process.env.VITE_DEFAULT_COUNTRY || 'KE_LOCAL';
const contractPath = path.join(__dirname, '..', 'src', 'config', 'taxonomyContract.js');
const outputPath = path.join(__dirname, '..', 'nginx.conf');

const content = fs.readFileSync(contractPath, 'utf-8');

// Find the country block and extract values from the ~2000 chars after the header
const headerPos = content.indexOf(`'${country}':`);
if (headerPos === -1) {
  console.error(`Country "${country}" not found in taxonomy contract`);
  process.exit(1);
}

const block = content.substring(headerPos, headerPos + 2000);

const backendUrl = block.match(/BACKEND_URL:\s*"([^"]+)"/)?.[1];
const backendPath = block.match(/BACKEND_PATH:\s*"([^"]+)"/)?.[1];
const amiHost = block.match(/AMI_HOST:\s*"([^"]+)"/)?.[1];

if (!backendUrl || !backendPath) {
  console.error('Could not extract BACKEND_URL or BACKEND_PATH from taxonomy contract');
  process.exit(1);
}

const url = new URL(backendUrl);
const backendHostname = url.hostname;

// Extract AMI port (default 8384)
let amiPort = '8384';
if (amiHost) {
  try {
    const amiUrl = new URL(amiHost.replace('wss://', 'https://'));
    if (amiUrl.port) amiPort = amiUrl.port;
  } catch (_) {}
}

console.log(`Generating nginx.conf for ${country}:`);
console.log(`  Backend: ${backendUrl}${backendPath}`);
console.log(`  Host: ${backendHostname}`);
console.log(`  AMI/ATI port: ${amiPort}`);

const nginxConf = `server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # API Proxy - Forward requests to backend
    location /api-proxy/ {
        proxy_pass ${backendUrl}${backendPath}/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_ssl_verify off;
        proxy_ssl_session_reuse on;
    }

    # WebSocket proxies (convert wss:// to https:// for proxy_pass)
    # proxy_read_timeout is critical for WebSockets — default 60s would kill
    # idle SIP/AMI connections, causing agents to drop from the queue.
    location /ws/ {
        proxy_pass ${backendUrl}/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_ssl_verify off;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }

    location /ami/ {
        proxy_pass https://${backendHostname}:${amiPort}/ami/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_ssl_verify off;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }

    location /ati/ {
        proxy_pass https://${backendHostname}:${amiPort}/ati/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_ssl_verify off;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
    }

    # Serve everything from root - Vite build puts files there
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Don't cache index.html
    location = /index.html {
        add_header Cache-Control "no-cache, no-store, must-revalidate";
        expires 0;
    }
}
`;

fs.writeFileSync(outputPath, nginxConf);
console.log('nginx.conf generated successfully');
