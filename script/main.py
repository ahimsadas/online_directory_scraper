import os
import requests
import csv

# Function to fetch data from the API
def fetch_data(query, page):
    url = f"https://6rhg85xpv5.execute-api.us-east-1.amazonaws.com/Prod/originators/?q={query}&page={page}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for query {query} and page {page}")
        print(f"Response: {response.json()}")
        raise Exception(f"Failed to fetch data for query {query} and page {page}. Status code: {response.status_code}")

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
        for i in range(97, 123):  # ASCII codes for lowercase letters a-z
            for j in range(97, 123):
                for k in range(97, 123):
                    query = chr(i) + chr(j) + chr(k)  # Generating query strings
                    page = 1
                    while True:
                        print(f"Fetching Data for: {query} and page: {page}")
                        data = fetch_data(query, page)
                        if data and 'data' in data and 'items' in data['data']:
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
                    query_count += 1
                    print(f"Progress: Query {query_count}/{total_queries} processed. Total data added: {total_data_count}\n\n")
    print("\nData retrieval and CSV creation completed. Total data added:", total_data_count)

if __name__ == "__main__":
    main()
