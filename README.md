# rpg-world-map

[![Run Unit Tests](https://github.com/renanstn/rpg-world-map/actions/workflows/test.yml/badge.svg)](https://github.com/renanstn/rpg-world-map/actions/workflows/test.yml)

## Objetivo

Construir uma ferramenta para mestres de RPG para que eles consigam criar seus
próprios mapas-mundis, especificando localizações e descrições.

Similar a isso: http://map.leagueoflegends.com/pt_BR

## Stack

Este projeto utiliza Docker e Docker Compose para manipular os diversos
containers (app, banco, bucket, etc)

Além disso, utiliza a seguinte stack:

- Python / Flask (backend)
- Postgres (banco de dados)
- Minio (bucket de arquivos)
- Railway (hospedagem)
- Github actions para pipelines de CI

## Fluxos

- Administrador acessa painel de admin
- Cria um `Mapa`
  - Insere o nome do mapa
  - Upload da imagem do mapa
  - Imagem é armazenada no Minio
  - Demais infos são armazenadas no Postgres
- O mestre recebe a url pública do mapa (para compartilhar com os jogadores)
- O mestre clica no mapa e vai adicionando `Points`, pontos de interesse
  - Define um ícone para o ponto de interesse
  - Define um nome para o ponto de interesse
  - Define uma descrição para o ponto de interesse

## Setup local

### Minio

Para que seja possível a aplicação acessar as imagens armazenadas no Minio, é
necessário dar permissão de download no bucket.

```sh
docker compose run --rm minio-mc alias set local http://minio:9000 minioadmin minioadmin
```

Dá permissão de download:

```sh
docker compose run --rm minio-mc anonymous set download local/rpg
```

UI do Minio acessível em:

http://localhost:9001

### Projeto

Subir projeto localmente

```sh
docker compose up -d
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

# Teste

1. Foo
1. Bar
1. Help!
