from google.cloud import secretmanager
import json
import os
PROJECT_ID = os.environ["_GCP_PROJECT_ID"]
def access_secret_version(secret_id, version_id="latest"):
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
    # Access the secret version.
    response = client.access_secret_version(name=name)

    # Return the decoded payload.
    response = response.payload.data.decode('UTF-8')
    try:
        response = json.loads(response)
    except:
        pass
    return response
