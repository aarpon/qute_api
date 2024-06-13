# ******************************************************************************
# Copyright © 2022 - 2024, ETH Zurich, D-BSSE, Aaron Ponti
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License Version 2.0
# which accompanies this distribution, and is available at
# https://www.apache.org/licenses/LICENSE-2.0.txt
#
# Contributors:
#   Aaron Ponti - initial API and implementation
# ******************************************************************************

import requests

# Define the URL to download the model from
base_url = "http://<server-ip>:5000/models"
model_name = "<model_name>"
version = "<version>"
url = f"{base_url}/{model_name}/{version}"

# Make a GET request to download the model
response = requests.get(url, stream=True)

# Check if the request was successful
if response.status_code == 200:
    # Define the path to save the downloaded model
    save_path = "path/to/save/model.ckpt"

    # Write the content to the file
    with open(save_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"Model saved to {save_path}")
else:
    print(f"Failed to download the model. Status code: {response.status_code}")
