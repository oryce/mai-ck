FROM node:22-alpine AS base

# Step 1. Rebuild the source code only when needed
FROM base AS builder

WORKDIR /app

COPY public ./public
COPY src ./src
COPY jsconfig.json .
COPY next.config.mjs .
COPY package.json .
COPY package-lock.json .
COPY postcss.config.mjs .

ENV NEXT_TELEMETRY_DISABLED 1

RUN npm ci
RUN npm run build

# Step 2. Production image, copy all the files and run Next
FROM base AS runner

WORKDIR /app

# Don't run production as root
RUN addgroup --system --gid 1001 nextjs
RUN adduser --system --uid 1001 nextjs
USER nextjs

COPY --from=builder /app/public ./public

# Automatically leverage output traces to reduce image size
# https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

ENV NEXT_TELEMETRY_DISABLED 1

CMD ["node", "server.js"]
