import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter } from 'k6/metrics';

const BASE_URL = __ENV.BASE_URL || 'https://jsonplaceholder.typicode.com';

export const statusCounter = new Counter('errors_by_status');

export const options = {
  stages: [
    { duration: '5s',  target: 10 },  // быстрый подъём до 10
    { duration: '30s', target: 10 },  // удерживаем 10 VUs (задание 1)
    { duration: '2s',  target: 50 },  // быстрый spike до 50
    { duration: '10s', target: 50 },  // держим 50 VUs (задание 2)
    { duration: '5s',  target: 0 },   // спуск
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], 
    http_req_failed: ['rate<0.01'],  
    checks: ['rate>0.99'],         
  },
};

export default function () {
  const res = http.get(`${BASE_URL}/posts`, {
    headers: { Accept: 'application/json' },
  });


  const ok = check(res, {
    'status is 200': (r) => r.status === 200,
    'content-type is json': (r) => {
      const ct = r.headers['Content-Type'] || r.headers['content-type'] || '';
      return ct.toLowerCase().includes('application/json');
    },
    'body contains array': (r) => {
      try {
        const b = JSON.parse(r.body);
        return Array.isArray(b);
      } catch (e) {
        return false;
      }
    },
  });

  if (!ok) {
    statusCounter.add(1, { status: String(res.status) });

    if (res.status !== 200) {
      console.error(`ERROR ${res.status}, body (truncated 200 chars): ${res.body ? res.body.slice(0,200) : 'empty'}`);
    }
  }

  sleep(1);
}