# Flask / Jinja2

---
## Flask와 Jinja2를 사용한 백엔드 서버 구축
=> WebSocket으로 프론트와 실시간 동기화

## React로 프론트엔드 구축

## 디렉토리 구성
flask-server
static/react
static/favicon.ico
static/logo192.png
templates/index.html


react-app
config
public
scripts
src

---
## 목표 : 웹 기반 인터페이스 구축 
원격 라즈베리파이 GPIO제어

## 사용방법 
react-app에서 npm run build 후
flask-server에서 OpenDashboard.py 실행 -> 13000번 포트에 웹서버 열 수 있음.