# Flask CRUD Architecture

## Before you start

Make sure you have Python 3.8 or higher installed on your machine.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the following command to start the server:

> Note: The server will run on port 5000 by default.

```bash
flask run
```

## Testing

Run the following command to run the tests:

```bash
pytest api_with_services/app/tests/integration.py -vv
```

## Endpoints

### POST /blog_posts

Creates a new blog post.

```bash
curl -d '{"title":"Test Title","content":"<h1>ContentTest</h1>","author_id":"author_123"}' -H "Content-Type: application/json" -X POST http://localhost:5000/blog_posts
```

Returns the following response:

```json
{
  "id": "37156588-aa00-4340-8423-366f459cf456",
  "author_id": "author_123",
  "content": "<h1>ContentTest</h1>",
  "title": "Test Title",
  "created_at": "2021-08-15T18:00:00.000000",
  "updated_at": "2021-08-15T18:00:00.000000"
}
```
