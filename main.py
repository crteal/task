'''A module definining a task based language to an LLM via an MCP server'''

import json
from pathlib import Path
from shutil import rmtree
import subprocess
from typing import Any, Callable
from mcp.server.fastmcp import FastMCP

DEFAULT_ENCODING = 'utf-8'


def make_task_success(
        task: dict[str, Any]
) -> dict[str, Any]:
    '''Makes a task success result.'''
    return {
        'id': task.get('id'),
        'action': task.get('action'),
        'success': True
    }


def make_task_error(
        task: dict[str, Any],
        type: str,
        message: str
) -> dict[str, Any]:
    '''Makes a task error result from `type` and `message`.'''
    return {
        'id': task.get('id'),
        'action': task.get('action'),
        'success': False,
        'error': {
            'type': type,
            'message': message
        }
    }


TASK_ACTION_HANDLERS = {}


def register_task_action_handler(
        action: str,
        handler: Callable[[dict[str, Any]], dict[str, Any]]
) -> None:
    '''Registers a `handler` by `action`'''
    if action in TASK_ACTION_HANDLERS:
        raise ValueError('A handler for `%s` already exists. Actions must be unique.' % (action,))
    TASK_ACTION_HANDLERS[action] = handler


def get_task_action_handler(
        action: str
) -> Callable[[dict[str, Any]], dict[str, Any]]:
    '''Gets a handler for `action` if it exists.'''
    if not action:
        raise ValueError('`handler` must be specified')

    if action not in TASK_ACTION_HANDLERS:
        raise ValueError('A handler for `%s` does not exist.' % (action,))

    return TASK_ACTION_HANDLERS.get(action)


def task_file_create(
        task: dict[str, Any]
) -> dict[str, Any]:
    '''A task to undertake file creation at a given path with optional content.'''
    if not task:
        return make_task_error(task, 'argument', '`task` must be specified')

    task_path = Path(task.get('path'))
    if task_path.exists():
        return make_task_error(
                task,
                'argument',
                'A file or directory at path `%s` already exists' % (task_path,)
        )

    content = task.get('content')
    # NOTE assume we are creating a new folder
    if not content:
        task_path.mkdir()
    else:
        encoding = content.get('encoding', DEFAULT_ENCODING)
        with task_path.open(mode='w', encoding=encoding) as f:
            f.write(content.get('value'))

    return make_task_success(task)


def task_file_edit(
        task: dict[str, Any]
) -> dict[str, Any]:
    '''A task to undertake file editing at a given path with content.'''
    if not task:
        return make_task_error(task, 'argument', '`task` must be specified')

    task_path = Path(task.get('path'))
    if not task_path.exists():
        return make_task_error(
                task,
                'argument',
                'A file or directory at path `%s` does not exist' % (task_path,)
        )

    if task_path.is_dir():
        return make_task_error(
                task,
                'argument',
                'A directory at path `%s` already exists' % (task_path,)
        )

    content = task.get('content')
    # NOTE assume we are creating a new folder
    if not content:
        return make_task_error(
                task,
                'argument',
                '`content` must exist for file editing'
        )

    encoding = content.get('encoding', DEFAULT_ENCODING)
    with task_path.open(mode='w', encoding=encoding) as f:
        f.write(content.get('value'))

    return make_task_success(task)


def task_file_delete(
        task: dict[str, Any]
) -> dict[str, Any]:
    '''A task to undertake file creation at a given path with optional content.'''
    if not task:
        return make_task_error(task, 'argument', '`task` must be specified')

    task_path = Path(task.get('path'))
    if not task_path.exists():
        return make_task_error(
                task,
                'argument',
                'A file or directory at path `%s` does not exist' % (task_path,)
        )

    if task_path.is_dir():
        rmtree(task_path)
    else:
        task_path.unlink()

    return make_task_success(task)


SAFE_COMMANDS = [
    'python',
    'node',
    'git',
    'uv'
]


def task_command_run(
        task: dict[str, Any]
) -> dict[str, Any]:
    '''A task to undertake running a command in a defined environment'''
    if not task:
        return make_task_error(task, 'argument', '`task` must be specified')

    cmd = task.get('command')
    if not cmd:
        return make_task_error(
                task,
                'argument',
                'A `command` must be specified'
        )

    if cmd not in SAFE_COMMANDS:
        return make_task_error(
                task,
                'argument',
                'The command `%s` is not currently available to run' % (cmd,)
        )

    cwd = task.get('path')
    env = task.get('environment')
    args = task.get('arguments', [])

    subprocess.run([cmd] + args, cwd=cwd, env=env, shell=True, check=True)

    return make_task_success(task)


TASKS = [
  # File related tasks
  ('file/create', task_file_create),
  ('file/edit', task_file_edit),
  ('file/delete', task_file_delete),

  # Command related tasks
  ('command/run', task_command_run)
]

for action, handler in TASKS:
    register_task_action_handler(action, handler)

mcp = FastMCP('task')


@mcp.resource('task://definition')
def get_definition() -> str:
    '''Gets the Task language definition'''
    with open('./resources/definition.md', mode='r', encoding='utf-8') as f:
        return f.read()


@mcp.tool()
def run_task(
        task: dict[str, Any]
) -> str:
    '''Runs the task specified by `task` and returns a result as a JSON string.'''
    if not task:
        raise ValueError('`task` must be specified')

    if not task.get('id'):
        raise ValueError('`task` must be have a `id` specified')

    handler = get_task_action_handler(task.get('action'))
    response = handler(task)
    return json.dumps(response)


if __name__ == "__main__":
    mcp.run(transport='stdio')
