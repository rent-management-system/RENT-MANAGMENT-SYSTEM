import os

def create_frontend_structure(root_path):
    frontend_structure = {
        "frontend": {
            "public": {
                "index.html": "",
                "favicon.ico": "",
                "manifest.json": ""
            },
            "src": {
                "assets": {
                    "images": {},
                    "styles": {}
                },
                "components": {
                    "auth": {
                        "Login.tsx": "",
                        "Register.tsx": "",
                        "GoogleCallback.tsx": ""
                    },
                    "common": {
                        "Button.tsx": "",
                        "Input.tsx": "",
                        "ErrorMessage.tsx": ""
                    },
                    "layout": {
                        "Navbar.tsx": "",
                        "Footer.tsx": ""
                    }
                },
                "pages": {
                    "Home.tsx": "",
                    "LoginPage.tsx": "",
                    "RegisterPage.tsx": "",
                    "Dashboard.tsx": "",
                    "Properties.tsx": ""
                },
                "context": {
                    "AuthContext.tsx": ""
                },
                "hooks": {
                    "useAuth.ts": "",
                    "useApi.ts": ""
                },
                "services": {
                    "api.ts": "",
                    "authService.ts": ""
                },
                "types": {
                    "auth.ts": "",
                    "property.ts": ""
                },
                "utils": {
                    "constants.ts": "",
                    "helpers.ts": ""
                },
                "App.tsx": "",
                "index.tsx": "",
                "main.css": "",
                "tailwind.config.js": ""
            },
            ".env": "",
            ".gitignore": "",
            "package.json": "",
            "tsconfig.json": "",
            "README.md": "",
            "postcss.config.js": ""
        }
    }

    def create_structure(base_path, structure):
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                create_structure(path, content)
            else:
                with open(path, 'w') as f:
                    f.write(content)

    frontend_path = os.path.join(root_path, "frontend")
    create_structure(root_path, frontend_structure)
    print(f"Frontend folder structure created successfully at {frontend_path}")

if __name__ == "__main__":
    root_path = "/home/dagi/Documents/Rent-managment-system"
    create_frontend_structure(root_path)