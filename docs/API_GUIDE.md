# API Reference Guide

## Base URL
`http://localhost:8000/api/v1`

## Authentication
All endpoints require the `X-API-Key` header.

## Endpoints
### 1. Generate Chart
`POST /ziwei/chart`
- **Request Body**: `{"year": 1988, "month": 8, "day": 18, "time_branch": "辰", "gender": "M"}`
- **Response**: `{ "status": "success", "ziwei_chart": {...}, "bazi_chart": {...} }`

### 2. Batch Upload
`POST /batch/upload`
- **Payload**: `multipart/form-data` with `file` field.
