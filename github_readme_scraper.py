from my_secrets.my_secrets import GITHUB_PAT
from bs4 import BeautifulSoup
import requests
import base64
import json
import os


API_URL = 'https://api.github.com'
HEADERS = {'Authorization': f'token {GITHUB_PAT}'}


def get_top_repos(limit=500):
    """Fetch top-starred public repositories, handling pagination."""
    repos = []
    page = 1
    while len(repos) < limit:
        response = requests.get(
            f'{API_URL}/search/repositories?q=stars:>1&sort=stars&per_page=100&page={page}',
            headers=HEADERS
        )
        if response.status_code != 200:
            break  # Break if there's an error
        current_page_repos = response.json()['items']
        repos.extend(current_page_repos)
        if len(current_page_repos) < 100:
            break  # Break if last page
        page += 1
    return repos[:limit]


def get_readme_content(repo):
    """Fetch README content in both Markdown and HTML format."""
    repo_name = repo['full_name']
    readme_url = f'{API_URL}/repos/{repo_name}/readme'
    readme_response = requests.get(readme_url, headers=HEADERS)

    if readme_response.status_code == 200:
        readme_md = base64.b64decode(readme_response.json()['content']).decode('utf-8')

        # Check if the README has 100 lines or less
        if len(readme_md.splitlines()) <= 100:
            # Render Markdown to HTML
            render_url = f'{API_URL}/markdown'
            html_response = requests.post(
                render_url,
                headers={'Authorization': f'token {GITHUB_PAT}'},
                json={'text': readme_md, 'mode': 'gfm'}
            )

            if html_response.status_code == 200:
                print("200 OK")
                return readme_md, html_response.text
            else:
                print(f"HTML RETRIVAL ERROR CODE {html_response.status_code }")
                return None, None
        else:
            print(f"ERROR THIS README HAS OVER 100 LINES: {len(readme_md.splitlines())}")
            return None, None
    else:
        print(f"MD RETRIEVAL CODE {readme_response.status_code}")
        return None, None


def save_to_jsonl(filename, data):
    """Save the JSONL data to a file."""
    # Create a directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as file:
        for line in data:
            file.write(line + '\n')


def is_valid_markdown(md):
    """Check if a string is likely valid Markdown. This is a basic check."""
    # Basic Markdown elements (you can expand this list)
    markdown_elements = ['*', '#', '-', '`', '```', '[', ']', '(', ')', '![']
    return any(element in md for element in markdown_elements)


def is_valid_html(html):
    """Check if a string is non-empty and looks like HTML."""
    basic_html_elements = ['<p>', '</p>']
    return any(element in html for element in basic_html_elements) and len(html) > 0


def create_jsonl_data():
    top_repos = get_top_repos()
    jsonl_data = []
    total_repos = len(top_repos)
    for idx, repo in enumerate(top_repos):
        print(f"Loading repo {idx + 1} / {total_repos}:")
        readme_md, readme_html = get_readme_content(repo)
        if readme_md and readme_html and is_valid_markdown(readme_md) and is_valid_html(readme_html):
            jsonl_data.append(json.dumps({
                "messages": [
                    {"role": "system", "content": "md2html"},
                    {"role": "user", "content": readme_md},
                    {"role": "assistant", "content": readme_html}
                ]
            }))
            print("\tOK")
        else:
            print("\tERROR")

    return jsonl_data


readmes_jsonl = create_jsonl_data()

# total = len(readmes_jsonl)
# for idx, line in enumerate(readmes_jsonl):
#     print(f"{idx + 1} / {total}: {line}")

save_to_jsonl('./data/readmes.jsonl', readmes_jsonl)
