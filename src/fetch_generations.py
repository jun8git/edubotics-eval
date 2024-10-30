import io
import os
import json
from literalai import LiteralClient

# Initialize the client with your API key
literalai_client = LiteralClient(api_key=os.environ['CD_AI_TUTOR_LITERAL_AI_API_KEY'])

# Function to create the logs directory if it doesn't exist
def create_logs_directory():
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    return logs_dir

# Function to fetch a batch of generations with pagination
def fetch_generations(limit=50, after_cursor=None):
    # Fetch generations with pagination
    result = literalai_client.api.get_generations(
        first=limit,
        after=after_cursor
    ).to_dict()
    return result

# Function to save generations to a JSON file
def save_generations_to_file(generations, page_info, file_index, logs_dir):
    filename = os.path.join(logs_dir, f'generations_{file_index}.json')
    data = {
        'data': generations,
        'pageInfo': page_info
    }
    with io.open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(generations)} generations to {filename}")

# Function to load the last downloaded file and get the endCursor
def get_last_endcursor(logs_dir):
    json_files = [f for f in os.listdir(logs_dir) if f.startswith('generations_') and f.endswith('.json')]
    if not json_files:
        return None, 0  # No previous files exist, start from the first batch

    json_files.sort()  # Sort files to get the latest one
    last_file = json_files[-1]

    with io.open(os.path.join(logs_dir, last_file), 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data['pageInfo']['endCursor'], int(last_file.split('_')[1].split('.')[0])

# Main function to download generations
def download_generations(batch_size=50):
    # Create the logs directory if it doesn't exist
    logs_dir = create_logs_directory()

    # Get the last endCursor and file index
    after_cursor, file_index = get_last_endcursor(logs_dir)

    has_next_page = True

    while has_next_page:
        # Fetch generations using the after_cursor from the last file
        result = fetch_generations(limit=batch_size, after_cursor=after_cursor)

        generations = result['data']
        page_info = result['pageInfo']
        has_next_page = page_info['hasNextPage']
        after_cursor = page_info['endCursor']

        # Save the generations to a new file in the logs directory
        file_index += 1
        save_generations_to_file(generations, page_info, file_index, logs_dir)

        print(f"Total batches downloaded: {file_index}")

# Entry point of the script
if __name__ == "__main__":
    import argparse

    # Parse the batch size from the command line
    parser = argparse.ArgumentParser(description="Download generations using Literal AI API")
    parser.add_argument("--batch_size", type=int, default=50, help="Number of generations to download per batch")

    args = parser.parse_args()

    # Call the download_generations function with the passed batch size
    download_generations(batch_size=args.batch_size)
