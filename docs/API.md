# Smart Store API

Authentication uses JWT.

## Token
`POST /api/token/`

## Refresh
`POST /api/token/refresh/`

## Products
`GET /api/products/`
`POST /api/products/`

## Sales
`GET /api/sales/`
`POST /api/sales/`

Creating a sale automatically reduces the associated product stock quantity.

## Analytics
`GET /api/analytics/summary/`

The summary contains product count, stock units, sales count, revenue, and products below their reorder threshold.
