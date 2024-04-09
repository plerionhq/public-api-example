import json
import time
import requests
import duckdb as db


def read_config(config_file):
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Config file '{config_file}' not found.")
        exit(1)


def write_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


class APIClient:
    def __init__(self, config):
        self.config = config
        self.base_url = f'https://{config["PlerionURL"]}'
        self.headers = {'Authorization': f"Bearer {config['PlerionAPIKey']}"}

    def get_paginated_data(self, path, params=None):
        data = []
        page = 1
        per_page = 500
        max_retries = 3
        retry_delay = 1

        while True:
            pagination_params = {'page': page, 'perPage': per_page}
            if params:
                pagination_params.update(params)

            for retries in range(max_retries):
                try:
                    print(f"Fetching page {page}...")
                    response = requests.get(
                        path, headers=self.headers, params=pagination_params)
                    response.raise_for_status()
                    response_data = response.json().get('data', [])
                    data.extend(response_data)

                    meta = response.json().get('meta', {})
                    if not meta.get('hasNextPage'):
                        return data

                    page += 1
                    break
                except requests.exceptions.RequestException as e:
                    print(f"Request failed: {e}")
                    time.sleep(retry_delay * (retries + 1))
            else:
                print("Max retries exceeded. Exiting...")
                break

        return data


def fetch_data(config_file='config.json'):
    config = read_config(config_file)
    api_client = APIClient(config)

    print('Fetching vulnerabilities with HIGH and CRITICAL severity levels...')
    vulnerabilities = api_client.get_paginated_data(
        f'{api_client.base_url}/v1/tenant/vulnerabilities',
        {'severityLevels': 'HIGH,CRITICAL',
         'hasExploit': 'true'})
    write_json('vulnerabilities.json', vulnerabilities)
    print(f'{len(vulnerabilities)} vulnerabilities fetched and saved to vulnerabilities.json')
    if not vulnerabilities:
        print('No vulnerabilities found. Exiting...')
        exit(0)

    print('Fetching assets that are publicly exposed...')
    assets = api_client.get_paginated_data(
        f'{api_client.base_url}/v1/tenant/assets',
        {'isPubliclyExposed': 'true'})
    write_json('assets.json', assets)
    print(f'{len(assets)} assets fetched and saved to assets.json')
    if not assets:
        print('No assets found. Exiting...')
        exit(0)


def main():
    fetch_data()

    vulnerabilities = db.query('''
        SELECT assetId,
            vulnerabilityId,
            severityLevel,
            severityLevelValue,
            severitySource,
            hasKev,
            hasExploit
        FROM read_json('vulnerabilities.json')''')

    assets = db.query('''
        SELECT id,
            name,
            type,
            fullResourceName,
            isPubliclyExposed
        FROM read_json('assets.json')''')

    report = db.query('''
        SELECT DISTINCT
            a.id AS assetId,
        FROM 
            assets a INNER JOIN vulnerabilities v 
        ON 
            a.id = v.assetId''')

    output_file = 'result.xlsx'
    db.sql(
        f"INSTALL spatial; LOAD spatial; COPY report TO '{output_file}' WITH (FORMAT GDAL, DRIVER 'xlsx');")
    print(f"Report saved to {output_file}")


if __name__ == "__main__":
    main()
