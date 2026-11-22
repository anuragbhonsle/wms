# WMS

## API routes (Currently)

- `GET /api/sellers` — returns all sellers.
- `GET /api/skus` — returns all SKUs.
- `GET /api/inwards/` — returns all inwards.
- `POST /api/inwards/` — creates an inward for a purchase order.

### Create an inward

Send a JSON request to `POST /api/inwards/`:

```json
{
  "po_id": 3,
  "user_id": 3,
  "status_id": 2
}
```

All three fields must be positive integer IDs for existing records. A successful
request returns `201 Created` with the new inward ID. Missing or invalid fields
return `400 Bad Request`; a referenced purchase order, user, or status that does
not exist returns `404 Not Found`.
