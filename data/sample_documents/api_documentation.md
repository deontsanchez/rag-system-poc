# REST API Documentation

## Overview
This API provides access to our customer management system. All endpoints require authentication and return JSON responses.

**Base URL:** `https://api.company.com/v1`

## Authentication
All API requests must include an API key in the header:
```
Authorization: Bearer YOUR_API_KEY
```

API keys can be obtained from the developer portal at https://developers.company.com

## Endpoints

### GET /customers
Retrieve a list of customers with optional filtering.

**Parameters:**
- `limit` (optional): Number of results to return (default: 50, max: 200)
- `offset` (optional): Number of results to skip for pagination (default: 0)
- `status` (optional): Filter by customer status (active, inactive, pending)
- `created_after` (optional): ISO 8601 date to filter customers created after this date

**Response:**
```json
{
  "data": [
    {
      "id": "cust_123",
      "name": "John Doe",
      "email": "john.doe@example.com",
      "status": "active",
      "created_at": "2023-01-15T10:30:00Z",
      "updated_at": "2023-06-20T14:45:00Z"
    }
  ],
  "pagination": {
    "limit": 50,
    "offset": 0,
    "total": 1250,
    "has_more": true
  }
}
```

### GET /customers/{id}
Retrieve details for a specific customer.

**Parameters:**
- `id` (required): Customer ID

**Response:**
```json
{
  "id": "cust_123",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1-555-0123",
  "address": {
    "street": "123 Main St",
    "city": "Anytown",
    "state": "CA",
    "zip": "12345",
    "country": "US"
  },
  "status": "active",
  "subscription": {
    "plan": "premium",
    "billing_cycle": "monthly",
    "next_billing_date": "2023-07-01T00:00:00Z"
  },
  "created_at": "2023-01-15T10:30:00Z",
  "updated_at": "2023-06-20T14:45:00Z"
}
```

### POST /customers
Create a new customer.

**Request Body:**
```json
{
  "name": "Jane Smith",
  "email": "jane.smith@example.com",
  "phone": "+1-555-0124",
  "address": {
    "street": "456 Oak Ave",
    "city": "Springfield",
    "state": "IL",
    "zip": "62701",
    "country": "US"
  }
}
```

**Response:**
```json
{
  "id": "cust_456",
  "name": "Jane Smith",
  "email": "jane.smith@example.com",
  "status": "pending",
  "created_at": "2023-07-21T15:20:00Z"
}
```

### PUT /customers/{id}
Update an existing customer.

**Parameters:**
- `id` (required): Customer ID

**Request Body:** Same as POST request, all fields optional

### DELETE /customers/{id}
Delete a customer (soft delete - marks as inactive).

**Parameters:**
- `id` (required): Customer ID

**Response:**
```json
{
  "message": "Customer successfully deleted",
  "deleted_at": "2023-07-21T15:25:00Z"
}
```

## Error Handling

### HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Rate Limited
- `500` - Internal Server Error

### Error Response Format
```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "The request is missing required parameters",
    "details": {
      "field": "email",
      "reason": "Email address is required"
    }
  }
}
```

## Rate Limiting
- 1000 requests per hour per API key
- Rate limit headers included in all responses:
  - `X-RateLimit-Limit`: Request limit per hour
  - `X-RateLimit-Remaining`: Requests remaining in current window
  - `X-RateLimit-Reset`: Unix timestamp when the limit resets

## SDKs and Libraries
Official SDKs available for:
- Python: `pip install company-api-python`
- JavaScript: `npm install @company/api-client`
- PHP: `composer require company/api-client`
- Ruby: `gem install company-api`

## Webhooks
Configure webhooks to receive real-time notifications of customer events:
- `customer.created`
- `customer.updated`
- `customer.deleted`
- `subscription.changed`

Webhook endpoints must respond with 200 status within 30 seconds.
