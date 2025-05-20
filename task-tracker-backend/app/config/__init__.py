from app.assistant.environment import env

config = {
  "database": {
    "engine": "postgresql",
    "host": env(f"TASK_DATABASE_HOST", "localhost"),
    "port": env(f"TASK_DATABASE_PORT", "54321"),
    "schema": env(f"TASK_DATABASE_SCHEMA", ""),
    "database_name": env(f"TASK_DATABASE_NAME", "task"),
    "username": env(f"TASK_DATABASE_USERNAME", "task"),
    "password": env(f"TASK_DATABASE_PASSWORD", "task")
  },
}

def get_config_params():  # pragma: unit
    """
    Gets the version of the application.
    """
    global config
    return config