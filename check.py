import re

def extract_citation_keys(latex_source):
    citation_pattern = r'\\(?:cite(?:[pt]?|author)?|nocite)\{([^}]+)\}'
    citation_keys = []
    for match in re.finditer(citation_pattern, latex_source):
        keys = match.group(1).split(',')
        citation_keys.extend(key.strip() for key in keys)
    return citation_keys

def extract_bibliography_keys(latex_source):
    bibliography_pattern = r'\\bibitem\{([^}]+)\}'
    bibliography_keys = []
    for match in re.finditer(bibliography_pattern, latex_source):
        keys = match.group(1)
        bibliography_keys.append(keys.strip())
    return bibliography_keys

def main():
    input_file = 'input/main.tex'  # Replace this with the path to your LaTeX source file

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            latex_source = file.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return

    citation_keys = extract_citation_keys(latex_source)
    bibliography_keys = extract_bibliography_keys(latex_source)

    # Check if the citations in the text match the bibliography
    citations_set = set(citation_keys)
    bibliography_set = set(bibliography_keys)

    if citations_set == bibliography_set:
        print("- All and only citations in the text are present in the bibliography.")
    else:
        missing_citations = citations_set - bibliography_set
        missing_bibliography = bibliography_set - citations_set
        print("- There are mismatches between bibliography and text_")
        if missing_citations:
            print(f"\tMissing in bibliography: {', '.join(missing_citations)}")
        if missing_bibliography:
            print(f"\tNot cited in text: {', '.join(missing_bibliography)}")
    
    common = citations_set & bibliography_set
    pre_citations = [item for item in citation_keys if item in common]
    pre_bibliography = [item for item in bibliography_keys if item in common]
    tmp = set()
    filtered_bibliography = []
    filtered_citations = []
    for i in pre_bibliography:
      if i not in tmp:
        filtered_bibliography.append(i)
        print(i)
      tmp.add(i)
    print("\n")
    
    tmp = set()
    for i in pre_citations:
      if i not in tmp:
        filtered_citations.append(i)
        print(i)
      tmp.add(i)
    
    
    # Check if the citations are sorted the same way
    if filtered_citations == filtered_bibliography:
        print("- Citations are sorted correctly.")
    else:
        print("- Citations are NOT sorted the same as in the bibliography.")

if __name__ == "__main__":
    main()
