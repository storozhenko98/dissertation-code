import os
import uuid
import subprocess

def quine():
    with open(__file__, 'r') as current_file:
        content = current_file.read()

    random_filename = str(uuid.uuid4()) + '.py'
    new_file_path = os.path.join(os.path.dirname(__file__), random_filename)
    with open(new_file_path, 'w') as new_file:
        new_file.write(content)

    subprocess.run(['python3', new_file_path])

quine()
