import sys
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql

def generate_postgres_schema(models_path="../model") -> list:
    table_info = {
        "User": "UserTable",
        "Task": "TaskTable",
    }

    for table_name, class_name in table_info.items():
        full_module_path = f"app.model.{table_name}"
        module = __import__(full_module_path, fromlist=[class_name])
        module_class = getattr(module, class_name)
        create_schema = CreateTable(module_class.__table__).compile(
            dialect=postgresql.dialect()
        )
        print(f"{create_schema};".replace("\n\n;", ";"))


if __name__ == "__main__":
    BASE_PATH = sys.argv[1] if len(sys.argv) > 1 else "../model"
    sys.path.append(BASE_PATH)
    generate_postgres_schema(BASE_PATH)