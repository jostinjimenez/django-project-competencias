import os

for root, dirs, files in os.walk("."):
    for file in files:
        if file.startswith("00") and file.endswith(".py") and file != "__init__.py":
            path = os.path.join(root, file)
            os.remove(path)
