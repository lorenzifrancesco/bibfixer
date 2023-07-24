import re

def extract_citation_keys(latex_source):
    citation_pattern = r'\\(?:cite(?:[pt]?|author)?|nocite)\{([^}]+)\}'
    citation_keys = []
    for match in re.finditer(citation_pattern, latex_source):
        keys = match.group(1).split(',')
        citation_keys.extend(key.strip() for key in keys)
    return citation_keys



def main():
    input_file = 'example/example.tex'  # Replace this with the path to your LaTeX source file
    output_file = 'citation_keys.txt'  # Replace this with the desired output file path

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            latex_source = file.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return

    citation_keys = extract_citation_keys(latex_source)

    try:
        with open(output_file, 'w', encoding='utf-8') as output:
            for key in citation_keys:
                output.write(key + '\n')
    except IOError:
        print(f"Error: Unable to write to '{output_file}'.")

    print(f"Citation keys have been saved to '{output_file}'.")

if __name__ == "__main__":
    main()
