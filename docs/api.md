# API Design
The API will be responsible for handling all requests from the frontend as an interface to the backend.
`// todo: this is all placeholder data as an example`

## API Routes
### User
| Route                          | Method      | Description                    |
| ------------------------------ | ----------- | ------------------------------ |
| `/api/v1/users`                | `GET`       | Get all users                  |
| `/api/v1/users`                | `POST`      | Create a new user              |
| `/api/v1/users/<id>`           | `GET`       | Get a user by ID               |
| `/api/v1/users/<id>`           | `PUT`       | Update a user by ID            |
| `/api/v1/users/<id>`           | `DELETE`    | Delete a user by ID            |

### Transaction
| Route                          | Method      | Description                    |
| ------------------------------ | ----------- | ------------------------------ |
| `/api/v1/transactions`         | `GET`       | Get all transactions           |
| `/api/v1/transactions`         | `POST`      | Create a new transaction       |
| `/api/v1/transactions/<id>`    | `GET`       | Get a transaction by ID        |
| `/api/v1/transactions/<id>`    | `PUT`       | Update a transaction by ID     |
| `/api/v1/transactions/<id>`    | `DELETE`    | Delete a transaction by ID     |

## API Models
### User
| Field                          | Type        | Description                    |
| ------------------------------ | ----------- | ------------------------------ |
| `id`                           | `int`       | User ID                        |
| `email`                        | `string`    | User's email                   |
| `username`                     | `string`    | User's username                |
| `avatar`                       | `string`    | User's avatar url              |
| `date_created`                 | `datetime`  | Date user was created          |
| `date_updated`                 | `datetime`  | Date user was last updated     |

### Transaction
| Field                          | Type        | Description                    |
| ------------------------------ | ----------- | ------------------------------ |
| `id`                           | `int`       | Transaction ID                 |
| `user_id`                      | `int`       | User ID                        |
| `amount`                       | `float`     | Transaction amount             |
| `date_created`                 | `datetime`  | Date transaction was created   |
| `date_updated`                 | `datetime`  | Date transaction was updated   |

## API Status Codes
| Code                           | Description                    |
| ------------------------------ | ------------------------------ |
| `200`                          | Success                        |
| `201`                          | Success + Created              |
| `400`                          | Bad Request                    |
| `401`                          | Unauthorized                   |
| `404`                          | Not Found                      |
| `500`                          | Internal Server Error          |

## API Responses
### Success (200, 201)
```json
{
  "status": 200, // or 201
  "message": "Success", // or Created
  "data": { /* data goes here */ }
}
```

### Error (400, 401, 404, 500)
```json
{
  "status": 400, // or 401, 404, 500
  "message": "Bad Request" // or Unauthorized, Not Found, Internal Server Error
  // notice no data property here
}
```
