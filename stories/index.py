import os
import datetime
from bs4 import BeautifulSoup

def extract_title(file_path):
    """Extract the title from an HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            title = soup.title.string if soup.title else "Untitled"
            return title.strip()
    except Exception as e:
        return f"Error reading title: {e}"

def read_intro():
    """Read the intro text from intro.html if it exists."""
    if os.path.exists('intro.html'):
        try:
            with open('intro.html', 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"<p>Error reading intro.html: {e}</p>"
    return "<p>Welcome! Below is the table of contents:</p>"

def generate_index():
    """Generate an index.html file with a table of contents."""
    html_files = [f for f in os.listdir() if f.endswith('.html') and f not in ('index.html', 'intro.html')]
    entries = []

    for html_file in html_files:
        title = extract_title(html_file)
        mod_time = os.path.getmtime(html_file)
        date_str = datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')
        entries.append((html_file, title, date_str))

    # Sort by modification date
    entries.sort(key=lambda x: x[2], reverse=True)

    # Read intro content
    intro_content = read_intro()

    # Generate HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Table of Contents</title>
    </head>
    <body>
        {intro_content}
        <h2>Table of Contents</h2>
        <ul>
    """
    for file_name, title, date in entries:
        html_content += f'            <li><a href="{file_name}">{title}</a> - {date}</li>\n'

    html_content += """
        </ul>
    </body>
    </html>
    """

    # Write to index.html
    with open('index.html', 'w', encoding='utf-8') as index_file:
        index_file.write(html_content)

    print("index.html has been generated successfully!")

if __name__ == "__main__":
    generate_index()
