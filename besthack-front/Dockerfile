FROM node:lts as dependencies
WORKDIR /besthack-front
COPY package.json package-lock.json ./
RUN npm install --force

FROM node:lts as builder
WORKDIR /besthack-front
COPY . .
COPY --from=dependencies /besthack-front/node_modules ./node_modules
RUN npm run build

FROM node:lts as runner
WORKDIR /besthack-front
ENV NODE_ENV production

COPY --from=builder /besthack-front/public ./public
COPY --from=builder /besthack-front/package.json ./package.json
COPY --from=builder /besthack-front/.next ./.next
COPY --from=builder /besthack-front/node_modules ./node_modules

EXPOSE 3000
CMD ["npm", "run", "start"]

