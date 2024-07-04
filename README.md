# degrabba

**Degrabba** is a Python script that enables users to identify which files a website fetches based on a specific search string.

## Getting started

A quick guide to get you started with **degrabba**.

1. Clone this GitHub repository.
2. Navigate to the repository's root directory.
3. Create a virtual environment by running the following command:

   ```bash
   python3 -m venv venv
   ```

4. Activate the virtual environment by running the following command:

   - Windows:

     ```bash
     venv\Scripts\activate
     ```

   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. Install the required packages by running the following command:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script by running the following command:

```bash
python3 degrabba.py -f <PATH_TO_FILE> -s <SEARCH_STRING>
```

- `<PATH_TO_FILE>`: The path to the file containing the URLs to be analyzed.
- `<SEARCH_STRING>`: The search string to be used to identify the files fetched by the website.

## Example usage

Example of command to run **degrabba**.

```bash
python3 degrabba.py -f urls.txt -s polyfill.io
```

## Output

### Console Output

- The script will output each URL and the files fetched by the website that contain the search string.
- At the end of the output, the script will print a summary of the affected URLs.

![Console Output](https://i.imgur.com/PHEb24I.png)

### File Output

- The script will also create a file named `result.json` containing the same information as the console output.

![File Output](https://i.imgur.com/jRrwIEh.png)

## Why this exists

I created
**degrabba** in response to a security incident where the cdn.polyfill.io domain injected malware into the polyfill.js library. To help developers ensure their websites are safe from such vulnerabilities, this tool identifies and flags external scripts fetched by a list of websites.

Read more about the incident [here](https://www.invicti.com/blog/web-security/polyfill-supply-chain-attack-when-your-cdn-goes-evil/).
