import requests
from bs4 import BeautifulSoup
import colorama
from colorama import Fore, Style
import argparse
import json

colorama.init(autoreset=True)

def read_web_pages(file_path):
    with open(file_path, 'r') as file:
        web_pages = [line.strip() for line in file.readlines()]
    
    for i, url in enumerate(web_pages):
        if not url.startswith('https://'):
            if url.startswith('http://'):
                web_pages[i] = url.replace('http://', 'https://')
            else:
                web_pages[i] = 'https://' + url
    
    return web_pages

def fetch_url(session, url, headers, timeout=3):
    try:
        response = session.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"{Fore.RED}An error occurred while processing {url}: {e}")
        return None

def find_string_in_js(url, search_string):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = fetch_url(session, url, headers)
    if response is None and url.startswith('https://'):
        url = url.replace('https://', 'http://')
        response = fetch_url(session, url, headers)
    
    if response is None:
        print(f"{Fore.RED}Timeout error for {url}")
        return []

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script', src=True)
        js_files = [script['src'] for script in scripts]
        files_with_search_string = [js_file for js_file in js_files if search_string in js_file]
        return files_with_search_string
    except Exception as e:
        print(f"{Fore.RED}An error occurred while processing {url}: {e}")
        return []
    finally:
        session.close()

def json_to_file(file, result):
    with open(file, "w") as f:
        json.dump(result, f, indent=4)

def main(file_path, search_string):
    web_pages = read_web_pages(file_path)

    print(f"{Fore.CYAN}Polyfill Searcher v1.0")
    print(f"{Fore.CYAN}Looking through {len(web_pages)} web page(s) for the string '{search_string}' in JavaScript files...")
    print("\n")
    
    result = {}
    for page in web_pages:
        print(f"Result for: {page}")
        files = find_string_in_js(page, search_string)
        
        if not files:
            print(f"{Fore.GREEN}No files found")
        
        if files:
            result[page] = files
            print(f'{Fore.CYAN}Found "{search_string}" in the following files:')
            for file in files:
                print(f"{Fore.YELLOW}{file}")
            
        print("\n")
        
    json_to_file("result.json", result)
    
    print(f"{Fore.CYAN}Affected web pages:")
    for key in result.keys():
        print(f"{Fore.RED}{key}")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search for a string in the URLs of JavaScript files on a list of web pages.')
    parser.add_argument('-f', '--file', type=str, required=True, help='Path to the file containing the list of web pages')
    parser.add_argument('-s', '--search-string', type=str, required=True, help='The search string to identify the URLs of files fetched by the website')
    args = parser.parse_args()
    
    main(args.file, args.search_string)
