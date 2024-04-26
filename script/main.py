import os
import requests
import csv
import time

# Function to fetch data from the API with retry logic
def fetch_data_with_retry(query, page):
    max_retries = 3
    retries = 0
    wait_time = 300 # Initial wait time in seconds (5 minutes)
    while retries < max_retries:
        url = f"https://6rhg85xpv5.execute-api.us-east-1.amazonaws.com/Prod/originators/?q={query}&page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            retries += 1
            if retries < max_retries:
                print(f"Failed to fetch data for query {query} and page {page}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                wait_time *= 2 # Double the wait time for next retry
            else:
                print(f"Failed to fetch data for query {query} and page {page} after {max_retries} retries.")
                return None

# Main function to iterate over queries and pages and save data to CSV
def main():
    # Create 'output' directory if not present
    if not os.path.exists('output'):
        os.makedirs('output')

    with open("output/all_data.csv", "w", newline="", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        total_data_count = 0
        total_queries = 26 ** 3
        query_count = 0
        for i in range(97, 123): # ASCII codes for lowercase letters a-z
            for j in range(97, 123):
                for k in range(97, 123):
                    query = chr(i) + chr(j) + chr(k) # Generating query strings
                    page = 1
                    while True:
                        print(f"Fetching Data for: {query} and page: {page}")
                        data = fetch_data_with_retry(query, page)
                        if data:
                            if 'data' in data and 'items' in data['data']:
                                data_count = len(data['data']['items'])
                                total_data_count += data_count
                                for item in data['data']['items']:
                                    writer.writerow(item.values())
                                if page == data['data']['last']:
                                    break
                                else:
                                    page += 1
                            else:
                                break
                        else:
                            # Retry the failed query from the beginning
                            page = 1
                            continue
                    query_count += 1
                    print(f"Progress: Query {query_count}/{total_queries} processed. Total data added: {total_data_count}\n\n")

    print("\nData retrieval and CSV creation completed. Total data added:", total_data_count)

if __name__ == "__main__":
    main()