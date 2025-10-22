# Fortuno Backend

Backend Django com Docker para o projeto Fortuno.

## Como executar

1. Build e execução com Docker Compose:
```bash
docker-compose up --build
```

2. Acesse: http://localhost:8000

## Comandos úteis

- Criar migrações: `docker-compose exec web python manage.py makemigrations`
- Aplicar migrações: `docker-compose exec web python manage.py migrate`
- Criar superuser: `docker-compose exec web python manage.py createsuperuser`