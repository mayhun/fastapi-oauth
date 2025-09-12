# social_login/Dockerfile
FROM nginx:1.27-alpine

# 정적 파일 복사
COPY . /usr/share/nginx/html/

# Nginx 설정 교체 (login.html을 기본 랜딩으로)
COPY nginx.conf /etc/nginx/nginx.conf
