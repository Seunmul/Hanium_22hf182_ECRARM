# Flask / Jinja2

---
## Flask와 Jinja2를 사용한 백엔드 서버 구축
=> WebSocket으로 프론트와 실시간 동기화

## React로 프론트엔드 구축

## 디렉토리 구성
flask-server
├── OpenDashboard.py
├── static
│   ├── favicon.ico
│   ├── logo192.png
│   └── react
└── templates
    └── index.html

react-app

.public
├── favicon.png
├── img
├── index.html
├── logo192.png
├── logo512.png
├── manifest.json
├── robots.txt
└── static
.src
├── App.css
├── App.js
├── components
│   ├── Sampletxt.js
│   ├── SignIn
│   ├── card
│   ├── divider
│   ├── footer
│   ├── icon
│   ├── main
│   ├── nav
│   └── sidebar
├── index.css
├── index.js
├── reducer
│   └── websocketReducer.js
├── store.js
└── websocket
    ├── _websocketContext.js
    ├── _websocket_legacy.js
    └── websocket.js

---
## 목표 : 웹 기반 인터페이스 구축 
원격 라즈베리파이 GPIO제어

## 사용방법 
react-app에서 npm run build 후
<<<<<<< HEAD
flask-server에서 OpenDashboard.py 실행 -> 80번 포트에 웹서버 열 수 있음.
=======
flask-server에서 OpenDashboard.py 실행 -> 80번 포트에 웹서버 열 수 있음.(배포용이면 sudo 명령 필요)
>>>>>>> dev
