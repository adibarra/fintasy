# API Design
The API is designed as a RESTful API. This means that it will be stateless and will use HTTP methods to interact with the backend. It is responsible for handling all frontend to backend interactions.
`// todo: this is all placeholder data as an example`

## API Routes
### User
| Route                          | Method      | Description                    |
| ------------------------------ | ----------- | ------------------------------ |
| `/api/v1/users`                | `POST`      | Create a new user              |
| `/api/v1/users/<id>`           | `GET`       | Get a user by ID               |
| `/api/v1/users/<id>`           | `PUT`       | Update a user by ID            |
| `/api/v1/users/<id>`           | `DELETE`    | Delete a user by ID            |

### Transaction
| Route                          | Method      | Description                    |
| ------------------------------ | ----------- | ------------------------------ |
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
| `200`                          | Ok                             |
| `400`                          | Bad Request                    |
| `401`                          | Unauthorized                   |
| `404`                          | Not Found                      |
| `500`                          | Internal Server Error          |

## API Response Types
### Success
```json
{
  "status": 200,
  "message": "Ok",
  "data": { /* data goes here */ }
}
```

### Error
```json
{
  "status": 400, // or 401, 404, 500
  "message": "Bad Request", // or Unauthorized, Not Found, Internal Server Error
  // no data property for errors
}
```
