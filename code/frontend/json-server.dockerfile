FROM node:22-alpine AS base

RUN npm install -g json-server

ENTRYPOINT ["npx", "json-server"]