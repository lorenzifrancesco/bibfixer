import re
from pybtex.database import parse_file, BibliographyData

def extract_citation_keys(bib_file_path):
    try:
        with open(bib_file_path, 'r', encoding='utf-8') as bib_file:
            bib_content = bib_file.read()
    except FileNotFoundError:
        print(f"Error: File '{bib_file_path}' not found.")
        return []

    # Regular expression pattern to find citation keys
    citation_pattern = r'@(\w+)\s*{([^,]+),'

    citation_keys = []
    modified_bib_content = bib_content
    for match in re.finditer(citation_pattern, bib_content):
        entry_type, entry_key = match.groups()
        # Make sure it's not a comment or preamble entry
        if not entry_key.startswith('@') and not entry_key.startswith('*'):
            citation_key = entry_key.strip().replace('_', '-')
            citation_keys.append(citation_key)
            # Replace the original key with the modified one in the .bib content
            modified_bib_content = modified_bib_content.replace(entry_key.strip(), citation_key)

    # Write the modified .bib content back to the file
    with open(bib_file_path, 'w', encoding='utf-8') as bib_file:
        bib_file.write(modified_bib_content)

    return citation_keys

def keep_fields_in_bib_file(input_file, output_file, fields_to_keep):
    bib_data = parse_file(input_file)

    for entry_key in bib_data.entries:
        entry = bib_data.entries[entry_key]
        for field in list(entry.fields.keys()):
            if field not in fields_to_keep:
                del entry.fields[field]

    bib_data.to_file(output_file)
    
def main():
    bib_file_path = 'example/sorted_ordered.bib'  # Replace this with the path to your .bib file

    citation_keys = extract_citation_keys(bib_file_path)

    if citation_keys:
        print("Modified citation keys written to the .bib file:")
        for key in citation_keys:
            print(key)
    else:
        print("No citation keys found in the .bib file.")
    
    fields_to_keep = ['author', 'title', 'date', 'journaltitle', 'pages', 'volume', 'number']  # Replace with the names of the fields you want to remove
    keep_fields_in_bib_file(bib_file_path, bib_file_path, fields_to_keep)
    keep_year_in_bib_file(bib_file_path, bib_file_path)
    add_comma_to_field_lines(bib_file_path)
if __name__ == "__main__":
    main()