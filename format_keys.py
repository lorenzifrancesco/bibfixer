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


def extract_year_from_date(date_str):
    # Function to extract the year from different date formats
    try:
        # Trying to parse the date in the format 'YYYY-MM-DD'
        return date_str.split('-')[0]
    except IndexError:
        pass

    try:
        # Trying to parse the date in the format 'YYYY/MM/DD'
        return date_str.split('/')[0]
    except IndexError:
        pass

    try:
        # Trying to parse the date in the format 'YYYY'
        return date_str
    except IndexError:
        pass

    # If the date cannot be parsed, return an empty string
    return ''

def keep_year_in_bib_file(input_file, output_file):
    bib_data = parse_file(input_file)

    for entry_key in bib_data.entries:
        entry = bib_data.entries[entry_key]
        for field in list(entry.fields.keys()):
            if field.lower() == 'date':
                # Keep only the year from the date field
                entry.fields[field] = extract_year_from_date(entry.fields[field])

    bib_data.to_file(output_file)

def add_comma_to_field_lines(bib_file_path):
    # Read the contents of the .bib file
    with open(bib_file_path, 'r') as f:
        bib_content = f.readlines()

    modified_lines = []

    # Iterate through each line in the .bib file
    for line in bib_content:
        line = line.strip()
        if line.startswith('@') or line.startswith('}'):
            # For entries or closing braces, we don't modify them
            modified_lines.append(line)
        elif line.endswith(','):
            # If the line already ends with a comma, we don't modify it
            modified_lines.append(line)
        elif len(line.strip())==0:
            modified_lines.append(line)
        else:
            # If the line doesn't end with a comma, we add one
            modified_lines.append(line + ',')

    # Write the modified content back to the .bib file
    with open(bib_file_path, 'w') as f:
        f.write('\n'.join(modified_lines))


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