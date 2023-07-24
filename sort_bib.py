import re

def read_citation_keys(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            citation_keys = [line.strip() for line in file]
        return citation_keys
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

def read_bib_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            bib_content = file.read()
        return bib_content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return ""

def sort_and_filter_bib_entries(citation_keys, bib_content):
    sorted_entries = []
    for key in citation_keys:
        pattern = r'(@\w+\s*{' + re.escape(key) + r',[^@]*})'
        match = re.search(pattern, bib_content, re.DOTALL)
        if match:
            sorted_entries.append(match.group(1))
    return sorted_entries

def main():
    citation_keys_file = 'citation_keys.txt'  # Replace this with the path to the citation keys file
    bib_file = 'example/example.bib'  # Replace this with the path to the BibLaTeX .bib file

    citation_keys = read_citation_keys(citation_keys_file)
    if not citation_keys:
        return

    bib_content = read_bib_file(bib_file)
    if not bib_content:
        return

    sorted_entries = sort_and_filter_bib_entries(citation_keys, bib_content)

    output_file = 'example/sorted_ordered.bib'  # Replace this with the desired output .bib file path
    try:
        with open(output_file, 'w', encoding='utf-8') as output:
            output.write('\n'.join(sorted_entries))
    except IOError:
        print(f"Error: Unable to write to '{output_file}'.")
        return

    print(f"The .bib entries have been sorted and filtered, and saved to '{output_file}'.")

if __name__ == "__main__":
    main()
