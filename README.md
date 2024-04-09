# public-api-example
## Summary

This Python script fetches assets and vulnerabilities from the Plerion Public API. It specifically targets assets with at least one exploitable vulnerability classified as having a High or Critical Severity Level. 

The vulnerability filters`{'severityLevels': 'HIGH,CRITICAL', 'hasExploit': 'true'} and asset filters `{'isPubliclyExposed': 'true'}` can be customized to your specific needs. Other options can be found in the API Reference section on the Plerion Resources page.

Finally, it exports the results to the `result.xlsx` Excel file.

## Note

The script assumes that the configuration file config.json exists in the same directory.
Ensure that the required permissions are granted to access the Plerion Public API.
Adjust the script as needed to suit specific requirements or environments.

## Running the Script

Follow these steps to execute the script:

1. **Create Virtual Environment**:
   - **Description**: Set up a virtual environment to isolate dependencies.
   - **Command**: `python -m venv .venv`

2. **Activate Virtual Environment**:
   - **Description**: Activate the virtual environment to use the installed dependencies.
   - **Command**: `source .venv/bin/activate`

3. **Install Dependencies**:
   - **Description**: Install required dependencies from the `requirements.txt` file.
   - **Command**: `pip install -r requirements.txt`

4. **Execute Script**:
   - **Description**: Run the Python script to perform desired operations.
   - **Command**: `python plerion.py`

## Creating the Public API Key

To create a Plerion Public API Key, follow these steps:

1. Navigate to "Tenant Settings" => "API Keys" in the Plerion Web UI.
2. Click on "Create API Key".
3. Provide a name for the API Key in the "API Key Name" field, and then click on "Create API Key".
4. Disable the "Base64 encoded JSON" toggle.
5. Click on "Copy as JSON", and paste the copied JSON into the `config.json` file.
  Note: The JSON data should include values for `PlerionURL`, `PlerionAPIKey`, `PlerionAccountId` and `ExternalId`. Only the first two are required.
6. Click on the "Confirm" button to finalize the creation process.
