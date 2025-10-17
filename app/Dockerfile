# ----------------------------
# 1️⃣ Build Stage
# ----------------------------
FROM node:24-alpine AS builder
WORKDIR /app
 
# Copy all files and install dependencies
COPY . .
RUN npm install
 
# Build your Vite project (creates /dist)
RUN npm run build
 
 
# ----------------------------
# 2️⃣ Run Stage
# ----------------------------
FROM node:18-alpine AS runner
WORKDIR /app
 
# Install a lightweight static file server
RUN npm install -g serve
 
# Copy build output from the builder stage
COPY --from=builder /app/dist ./dist
 
# Cloud Run sets PORT automatically (default 8080)
ENV PORT=8501
EXPOSE 8501
 
# Serve static files
CMD ["serve", "dist", "-l", "tcp://0.0.0.0:8501"]