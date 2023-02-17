import subprocess

def lambdaFunction(event):
    # Read secrets from secrets.txt file
    with open('secrets.txt', 'r') as f:
        secrets = f.readlines()
        username = secrets[0].strip()
        password = secrets[1].strip()

    # Define Docker run command with environmental overrides
    docker_command = [
        'docker', 'run',
        '-e', f'USERNAME={username}',
        '-e', f'PASSWORD={password}',
        'my-docker-image'
    ]

    # Run Docker container
    try:
        result = subprocess.run(docker_command, capture_output=True, check=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stderr)
