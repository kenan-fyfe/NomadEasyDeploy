import getpass
import requests

def get_deployment_details():
    deployment_details = {}

    deployment_details['job_name'] = input("Enter the job name: ")
    deployment_details['task_group'] = input("Enter the task group name: ")
    deployment_details['image'] = input("Enter the Docker image URL: ")
    deployment_details['cpu'] = input("Enter the CPU resources (in MHz): ")
    deployment_details['memory'] = input("Enter the memory resources (in MB): ")
    deployment_details['num_instances'] = input("Enter the number of instances: ")
    deployment_details['port'] = input("Enter the exposed port number: ")

    # Optionally, you can prompt for authentication details
    auth_required = input("Is authentication required? (Y/N): ")
    if auth_required.upper() == "Y":
        deployment_details['username'] = input("Enter the username: ")
        deployment_details['password'] = getpass.getpass("Enter the password: ")

    return deployment_details

def deploy_application(deployment_details):
    url = "http://nomad-api.example.com/v1/jobs"  # Replace with the actual Nomad API endpoint
    headers = {'Content-Type': 'application/json'}

    # Create the Nomad job payload using the deployment details
    job_payload = {
        "Job": {
            "ID": deployment_details['job_name'],
            "Name": deployment_details['job_name'],
            "Type": "service",
            "Datacenters": ["dc1"],
            "TaskGroups": [
                {
                    "Name": deployment_details['task_group'],
                    "Tasks": [
                        {
                            "Name": deployment_details['task_group'],
                            "Driver": "docker",
                            "Config": {
                                "image": deployment_details['image'],
                                "port_map": [{"http": int(deployment_details['port'])}]
                            },
                            "Resources": {
                                "CPU": int(deployment_details['cpu']),
                                "MemoryMB": int(deployment_details['memory']),
                                "Networks": [{"MBits": 10, "DynamicPorts": ["http"]}]
                            },
                            "Env": {
                                "SOME_ENV_VAR": "some_value"
                            }
                        }
                    ],
                    "Count": int(deployment_details['num_instances'])
                }
            ]
        }
    }

    if 'username' in deployment_details:
        auth = (deployment_details['username'], deployment_details['password'])
        response = requests.post(url, json=job_payload, headers=headers, auth=auth)
    else:
        response = requests.post(url, json=job_payload, headers=headers)

    if response.status_code == 200:
        return True
    else:
        print("Error deploying the application:")
        print(response.text)
        return False

def main():
    print("=== HashiCorp Nomad Application Deployment ===")
    deployment_details = get_deployment_details()

    if deploy_application(deployment_details):
        print("Deployment successful!")
        print("Job Name:", deployment_details['job_name'])
        print("Task Group:", deployment_details['task_group'])
        print("Image:", deployment_details['image'])
        print("CPU:", deployment_details['cpu'])
        print("Memory:", deployment_details['memory'])
        print("Number of Instances:", deployment_details['num_instances'])
        print("Port:", deployment_details['port'])
        if 'username' in deployment_details:
            print("Username:", deployment_details['username'])
            print("Password: ********")  # Password is masked for security

if __name__ == "__main__":
    main()
