# rpg-world-map

## Objetivo

Construir uma ferramenta para mestres de RPG para que eles consigam criar seus próprios mapas-mundis, especificando localizações e descrições.

## Stack

Este projeto provavelmente usará:

- JavaScript (frontend)
- Python (backend)
- Postgres (banco de dados)
- Minio / S3 (bucket de arquivos)
- Railway (hospedagem)

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

## Setup

TODO
