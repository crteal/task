<TASK>
# Task

The following JavaScript Object Notation (JSON) describes a Task request designed for automation (agents).

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://dev.crteal.com/task.schema.json",
  "title": "Task Request",
  "description": "A task request articulating an operation or command to execute.",
  "type": "object",
  "properties": {
    "id": {
      "description": "The unique identifier for a task request",
      "type": "string"
    },
    "action": {
      "description": "The type of task to execute",
      "type": "string"
    },
    "arguments": {
      "description": "The arguments to pass the command during execution",
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "path": {
      "description": "The working or output path",
      "type": "string"
    },
    "command": {
      "description": "The binary or script to execute",
      "type": "string"
    },
    "content": {
      "description": "The working or output path",
      "type": "object",
      "properties": {
        "encoding": {
          "type": "string"
        },
        "value": {
          "type": "string"
        }
      }
    },
    "environment": {
      "description": "The environment to use during command execution",
      "type": "object"
    }
  }
}
```

Available actions are `file/create`, `file/edit`, `file/delete`, and `command/run`. For each of these there are examples below.

<EXAMPLE>
## `file/create`, File/Directory Creation

<REQUEST>
Create a new directory...
```javascript
{
    "id": "0195c73c-ba9c-7fc3-94d8-c7367d968b32",
    "action": "file/create",
    "path": "/tmp/demo"
}
```

Create a new Python file...

```javascript
{
    "id": "0195c73c-ba9c-7fc3-94d8-c7367d968b32",
    "action": "file/create",
    "path": "/tmp/demo/foo.py",
    "content": {
        "encoding": "utf-8",
        "value": 'print("hello world")'
    }
}
```
</REQUEST>
<RESPONSE>
Success

```javascript
{
    "id": "0195c73c-ba9c-7fc3-94d8-c7367d968b32",
    "action": "file/create",
    "success": true
}
```

Error
```javascript
{
    "id": "0195c73c-ba9c-7fc3-94d8-c7367d968b32",
    "action": "file/create",
    "success": false,
    "error": {
        "type": "PERMISSION_ERROR"
        "message": "the user does not have permissions"
    }
}
```
</RESPONSE>
</EXAMPLE>

<EXAMPLE>
## `file/edit`, File Editing

<REQUEST>
```javascript
{
    "id": "0195c73c-ba9c-7fcf-9eba-ce12c2f266c5",
    "action": "file/edit",
    "path": "/tmp/demo/foo.py",
    "content": {
        "encoding": "utf-8",
        "value": 'print("hello, world")'
    }
}
```
</REQUEST>
<RESPONSE>
Success

```javascript
{
    "id": "0195c73c-ba9c-7fcf-9eba-ce12c2f266c5",
    "action": "file/edit",
    "success": true
}
```

Error
```javascript
{
    "id": "0195c73c-ba9c-7fcf-9eba-ce12c2f266c5",
    "action": "file/edit",
    "success": false,
    "error": {
        "type": "PERMISSION_ERROR"
        "message": "the user does not have permissions"
    }
}
```
</RESPONSE>
</EXAMPLE>
<EXAMPLE>
## `file/delete`, File Deletion

<REQUEST>
```javascript
{
    "id": "0195c73c-ba9c-70b1-9233-a97050cf775c",
    "action": "file/delete",
    "path": "/tmp/demo/foo.py"
}
```
</REQUEST>
<RESPONSE>
Success

```javascript
{
    "id": "0195c73c-ba9c-70b1-9233-a97050cf775c",
    "action": "file/delete",
    "success": true
}
```

Error
```javascript
{
    "id": "0195c73c-ba9c-70b1-9233-a97050cf775c",
    "action": "file/delete",
    "success": false,
    "error": {
        "type": "PERMISSION_ERROR"
        "message": "the user does not have permissions"
    }
}
```
</RESPONSE>
</EXAMPLE>
<EXAMPLE>
## `command/run`, Command Run

<REQUEST>
Initializes a Git repository

```javascript
{
    "id": "0195c74b-93b2-7cb1-ace7-75fd8fe905f6",
    "action": "command/run",
    "arguments": ["init"],
    "command": "git",
    "path": "/tmp/demo"
}
```

Run a Node.js file with an environment variable
```javascript
{
    "id": "0195c74b-93b2-7d64-9d02-8410a3164641",
    "action": "command/run",
    "arguments": ["server.js"],
    "environment": {
        "PORT": 5000
    },
    "command": "node",
    "path": "/tmp/demo"
}
```

Run a Node.js file with additional arguments
```javascript
{
    "id": "0195c74b-93b3-7f18-9e67-a4ca2a568409",
    "action": "command/run",
    "arguments": [
        "server.js",
        "--port 5000"
    ],
    "command": "node",
    "path": "/tmp/demo"
}
```
</REQUEST>
<RESPONSE>
Success

```javascript
{
    "id": "0195c74b-93b2-7cb1-ace7-75fd8fe905f6",
    "action": "command/run",
    "success": true
}
```

Error
```javascript
{
    "id": "0195c74b-93b2-7d64-9d02-8410a3164641",
    "action": "command/run",
    "success": false,
    "error": {
        "type": "PERMISSION_ERROR"
        "message": "the user does not have permissions"
    }
}
```
</RESPONSE>
</EXAMPLE>
</TASK>
