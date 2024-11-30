# import zipfile
# import re
# import os

# def extract_class_names(jar_path):
#     class_names = []
#     with zipfile.ZipFile(jar_path, 'r') as jar:
#         for file_info in jar.infolist():
#             if file_info.filename.endswith('.class'):
#                 class_name = file_info.filename.replace('/', '.').rstrip('.class')
#                 class_names.append(class_name)
#     return class_names

# def extract_private_methods(jar_path):
#     private_methods = []
#     with zipfile.ZipFile(jar_path, 'r') as jar:
#         for file_info in jar.infolist():
#             if file_info.filename.endswith('.class'):
#                 with jar.open(file_info) as class_file:
#                     class_data = class_file.read()
#                     methods = re.findall(b'\x2d\x00[\x00-\xff]{2}', class_data)
#                     for method in methods:
#                         private_methods.append(method)
#     return private_methods
# if __name__ == "__main__":
#     jar_path = 'chess-0.0.2-SNAPSHOT.jar'  # Replace with the path to your JAR file
#     class_names = extract_class_names(jar_path)
#     for class_name in class_names:
#         print(class_name)

#     private_methods = extract_private_methods(jar_path)
#     for method in private_methods:
#         print(method)

#================================================================================================

import os
import subprocess
import zipfile
import tempfile
import re

def extract_private_methods(jar_path):
    if not os.path.isfile(jar_path):
        print(f"File not found: {jar_path}")
        return

    private_methods = {}

    # Regular expression to identify methods (e.g., private void methodName() or private int methodName(params))
    method_pattern = re.compile(r"private\s+[\w<>\[\]]+\s+\w+\(.*\)")

    # Create a temporary directory to extract the JAR
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(jar_path, 'r') as jar:
            jar.extractall(temp_dir)

        # Walk through all extracted files
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.endswith('.class'):
                    class_file = os.path.join(root, file)

                    # Use javap to extract class details
                    try:
                        result = subprocess.run(
                            ["javap", "-private", class_file],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True
                        )

                        # Parse the output for private methods
                        output = result.stdout
                        methods = method_pattern.findall(output)
                        if methods:
                            class_name = os.path.relpath(class_file, temp_dir).replace("/", ".").replace("\\", ".").replace(".class", "")
                            private_methods[class_name] = methods
                    except Exception as e:
                        print(f"Error processing {class_file}: {e}")

    return private_methods


# Path to your JAR file
jar_file_path = "chess-0.0.2-SNAPSHOT.jar"  # Replace with your JAR file path

# Extract private methods
private_methods = extract_private_methods(jar_file_path)

# Display the results
if private_methods:
    for class_name, methods in private_methods.items():
        print(f"\nClass: {class_name}")
        for method in methods:
            print(f"  {method}")
else:
    print("No private methods found or an error occurred.")