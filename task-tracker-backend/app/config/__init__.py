from app.assistant.environment import env

config = {
  "database": {
    "engine": "postgresql",
    "host": env("TASK_TRACKER_HOST", "database"),
    "port": env("TASK_TRACKER_PORT", "5432"),
    "schema": env("TASK_TRACKER_SCHEMA", "public"),
    "database_name": env("TASK_TRACKER_NAME", "task-tracker"),
    "username": env("TASK_TRACKER_USERNAME", "task-tracker"),
    "password": env("TASK_TRACKER_PASSWORD", "task-tracker")
  },
}

def get_config_params():  # pragma: unit
    """
    Gets the version of the application.
    """
    global config
    return config