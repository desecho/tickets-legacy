FROM tickets:latest as tickets_app

FROM nginx:alpine 

COPY --from=tickets_app /app/static /usr/share/nginx/html
