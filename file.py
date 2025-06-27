import os

project_root = "Rent-managment-system"
backend_path = os.path.join(project_root, "backend")

folders = [
    os.path.join(backend_path, "app", "routers"),
    os.path.join(backend_path, "tests"),
]

files = {
    os.path.join(backend_path, "app", "__init__.py"): "",
    os.path.join(backend_path, "app", "main.py"): "# Entry point for FastAPI app\n",
    os.path.join(backend_path, "app", "routers", "__init__.py"): "",
    os.path.join(backend_path, "app", "routers", "auth.py"): "# Authentication endpoints\n",
    os.path.join(backend_path, "app", "routers", "users.py"): "# User management endpoints\n",
    os.path.join(backend_path, "app", "routers", "properties.py"): "# Property-related endpoints\n",
    os.path.join(backend_path, "app", "dependencies.py"): "# Dependency functions\n",
    os.path.join(backend_path, "app", "schemas.py"): "# Pydantic models\n",
    os.path.join(backend_path, "app", "crud.py"): "# CRUD operations\n",
    os.path.join(backend_path, "app", "models.py"): "# SQLAlchemy models\n",
    os.path.join(backend_path, "app", "database.py"): "# Database connection\n",
    os.path.join(backend_path, "tests", "__init__.py"): "",
    os.path.join(backend_path, "tests", "test_main.py"): "# Tests for main endpoints\n",
    os.path.join(backend_path, ".env"): "# Environment variables\n",
    os.path.join(backend_path, "requirements.txt"): "# Backend dependencies\n",
    os.path.join(backend_path, "README.md"): "# Backend documentation\n",
    os.path.join(project_root, "README.md"): "# Project-level documentation\n",
}

# Create directories
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files with placeholder content
for file_path, content in files.items():
    with open(file_path, "w") as f:
        f.write(content)

print("✅ Project structure created under 'Rent-managment-system/backend/'")
