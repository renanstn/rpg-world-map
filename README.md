# rpg-world-map

[![Run Unit Tests](https://github.com/renanstn/rpg-world-map/actions/workflows/test.yml/badge.svg)](https://github.com/renanstn/rpg-world-map/actions/workflows/test.yml)

## Objetivo

Construir uma ferramenta para mestres de RPG para que eles consigam criar seus
próprios mapas-mundis, especificando localizações e descrições.

Similar a isso: http://map.leagueoflegends.com/pt_BR

## Stack

Este projeto provavelmente usará:

- JavaScript (frontend)
- Python (backend)
- Postgres (banco de dados)
- Minio / S3 (bucket de arquivos)
- Railway (hospedagem)
- Github actions para pipelines de CI

## Fluxos

- Administrador acessa painel de admin
- Cria um `Mapa`
  - None
  - Upload da imagem
  - Tamanho do mapa é definido pelo tamanho da imagem
  - Imagem é armazenada no Minio
- Recebe a url pública do mapa (para compartilhar com os jogadores)
- Clica no mapa e vai adicionando `Points`, pontos de interesse
  - Define um ícone para o ponto de interesse
  - Define um nome para o ponto de interesse
  - Define uma descrição para o ponto de interesse

## Setup local

```sh
docker compose up
```

## Comandos úteis de desenvolvimento

Rode eles dentro da pasta `src/`

### Formatar código automaticamente

```sh
make format
```

### Rodar testes

```sh
docker compose run --rm flask-app pytest
```

## Comandos CURL para testar a API

Preguiça de instalar o Postman, vai via CURL mesmo...

Ping

```sh
curl http://localhost:5000/
```
