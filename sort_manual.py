import re

def read_citation_keys(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            citation_keys = [line.strip() for line in file]
        return citation_keys
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

def read_tex_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tex_content = file.read()
        return tex_content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return ""

def sort_and_filter_bibitems(citation_keys, tex_content):
    sorted_entries = []
    for key in citation_keys:
        # Regular expression to find \bibitem{key} entries
        # pattern = r'(\\bibitem\s*{' + re.escape(key) + r'}(?:[^\\]+|\n(?!\\))*\n?)'
        pattern = r'(\\bibitem\s*{' + re.escape(key) + r'}\s*\n[^\n]*)'
        match = re.search(pattern, tex_content, re.DOTALL)
        if match:
            sorted_entries.append(match.group(1)+'\n')
    return sorted_entries

def main():
    citation_keys_file = 'output/unique_citation_keys.txt'  # Replace this with the path to the citation keys file
    tex_file = 'input/main_manual.tex'  # Replace this with the path to the .tex file

    citation_keys = read_citation_keys(citation_keys_file)
    if not citation_keys:
        return

    tex_content = read_tex_file(tex_file)
    if not tex_content:
        return

    sorted_entries = sort_and_filter_bibitems(citation_keys, tex_content)

    output_file = 'output/sorted_manual.tex'  # Replace this with the desired output .tex file path
    try:
        with open(output_file, 'w', encoding='utf-8') as output:
            output.write('\n'.join(sorted_entries))
    except IOError:
        print(f"Error: Unable to write to '{output_file}'.")
        return

    print(f"The \\bibitem entries have been sorted and filtered, and saved to '{output_file}'.")

if __name__ == "__main__":
    main()
