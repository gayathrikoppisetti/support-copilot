---
title: Taskly API Documentation
doc_type: api_docs
last_updated: 2026-05-20
access_level: public
---

# Taskly REST API

Base URL: https://api.taskly.example/v2

## Authentication
Send your API token in the Authorization header as a Bearer token. Create tokens under Settings, then Developer, then API Tokens. If your token is invalid, the API returns HTTP 401 with error code E-4010.

## Endpoints

### GET /v2/tasks
Returns a paginated list of tasks. Supports the query parameters project_id, assignee, status, and limit (maximum 100).

### POST /v2/tasks
Creates a task. Required fields: title and project_id. Optional fields: assignee, due_date, labels.

### PATCH /v2/tasks/{id}
Updates an existing task. Send only the fields you want to change.

### DELETE /v2/tasks/{id}
Deletes a task permanently. This cannot be undone.

## Rate limits
Pro plans are limited to 60 requests per minute. Business plans are limited to 300 requests per minute. If you exceed the limit, the API returns HTTP 429 with error code E-4290. Wait for the number of seconds in the Retry-After header before trying again.

## Webhooks
Taskly can send a POST request to your server when a task is created, updated, or completed. Configure webhook URLs under Settings, then Developer.
