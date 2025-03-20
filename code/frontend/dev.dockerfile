FROM node:22-alpine

WORKDIR /app

COPY public ./public
COPY src ./src
COPY jsconfig.json .
COPY mock-db.json .
COPY next.config.mjs .
COPY package.json .
COPY package-lock.json .
COPY postcss.config.mjs .

ENV NEXT_TELEMETRY_DISABLED 1

RUN npm ci

CMD ["npm", "run", "dev"]
