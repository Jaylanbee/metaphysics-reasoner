# Metaphysics-Reasoner v3.1 Deployment Guide

This guide provides instructions for deploying the platform via Docker.

## Prerequisites
- Docker & Docker Compose
- Node 18+ (if building frontend manually)
- Python 3.10+ (if running backend manually)

## Environment Setup
1. Copy `.env.example` to `.env.prod`.
2. Edit `.env.prod` to include your secure `API_KEY` and LLM configurations.

## Docker Deployment (30-Minute Setup)
1. Build and start the containers:
   ```bash
   docker-compose up -d --build
   ```
2. Verify running services:
   ```bash
   docker ps
   ```
   You should see `backend`, `frontend`, `redis`, and `chromadb` all running and healthy.

## Monitoring & Health Checks
- **Health Check**: `curl http://localhost:8000/health`
- **Prometheus Metrics**: `curl http://localhost:8000/metrics`

## Troubleshooting
- If the backend cannot connect to the database, ensure `data/ziwei_universe_518k.db` exists.
- If Redis connection fails, check the docker-compose logs: `docker-compose logs redis`.
