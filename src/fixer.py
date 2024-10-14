import os
import re


def list_tex_files(folder_path):
    # List all .tex files in the given folder
    tex_files = [f for f in os.listdir(folder_path) if f.endswith('.tex')]

    if not tex_files:
        print("No .tex files found in the folder.")
        return None

    # Display the .tex files as options
    print("Select a .tex file:")
    for idx, file in enumerate(tex_files):
        print(f"{idx + 1}: {file}")

    # Get user's choice
    while True:
        try:
            choice = int(
                input("\nEnter the number corresponding to the file: ")) - 1
            if 0 <= choice < len(tex_files):
                return folder_path+tex_files[choice]
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")


class ManualBibFixer:

    def __init__(self) -> None:
        folder_path = "./input/"
        self.main = list_tex_files(folder_path)
        self.keys = "output/citation_keys.txt"
        self.unique_keys = "output/unique_citation_keys.txt"
        self.sorted = "output/sorted.tex"
        
        
    def extract(self):
        try:
            with open(self.main, 'r', encoding='utf-8') as file:
                latex_source = file.read()
        except FileNotFoundError:
            print(f"Error: File '{self.main}' not found.")
            return

        citation_pattern = r'\\(?:cite(?:[pt]?|author)?|nocite)\{([^}]+)\}'
        citation_keys = []
        for match in re.finditer(citation_pattern, latex_source):
            keys = match.group(1).split(',')
            citation_keys.extend(key.strip() for key in keys)
        try:
            with open(self.keys, 'w', encoding='utf-8') as output:
                for key in citation_keys:
                    output.write(key + '\n')
            with open(self.unique_keys, 'w', encoding='utf-8') as output:
                prev_key = set()
                for key in citation_keys:
                    if key not in prev_key:
                        output.write(key + '\n')
                        prev_key.add(key)
        except IOError:
            print(f"Error: Unable to write to '{self.keys}'.")

        print(
            f"- Citation keys have been saved to '{self.keys}' and '{self.unique_keys}'.")
    
    
    def sort(self):
      citation_keys = self.read_unique_citation_keys()
      tex_content = self.read_tex_file()
      sorted_entries = self.sort_and_filter_bibitems(citation_keys, tex_content)
      try:
          with open(self.sorted, 'w', encoding='utf-8') as output:
              output.write('\n'.join(sorted_entries))
      except IOError:
          print(f"Error: Unable to write to '{self.sorted}'.")
      print(f"- The \\bibitem entries have been sorted and filtered, and saved to '{self.sorted}'.")


    def read_unique_citation_keys(self):
        try:
            with open(self.unique_keys, 'r', encoding='utf-8') as file:
                citation_keys = [line.strip() for line in file]
            return citation_keys
        except FileNotFoundError:
            return []


    def read_tex_file(self):
        try:
            with open(self.main, 'r', encoding='utf-8') as file:
                tex_content = file.read()
            return tex_content
        except FileNotFoundError:
            return ""


    def sort_and_filter_bibitems(self, citation_keys, tex_content):
        sorted_entries = []
        for key in citation_keys:
            pattern = r'(\\bibitem\s*{' + re.escape(key) + r'}\s*\n[^\n]*)'
            match = re.search(pattern, tex_content, re.DOTALL)
            if match:
                sorted_entries.append(match.group(1)+'\n')
        return sorted_entries
      
      
    def extract_citation_keys(self):
      citation_pattern = r'\\(?:cite(?:[pt]?|author)?|nocite)\{([^}]+)\}'
      citation_keys = []
      for match in re.finditer(citation_pattern, self.main):
          keys = match.group(1).split(',')
          citation_keys.extend(key.strip() for key in keys)
      return citation_keys


    def extract_bibliography_keys(self):
        bibliography_pattern = r'\\bibitem\{([^}]+)\}'
        bibliography_keys = []
        for match in re.finditer(bibliography_pattern, self.main):
            keys = match.group(1)
            bibliography_keys.append(keys.strip())
        return bibliography_keys


    def check(self):
      citation_keys = self.extract_citation_keys()
      bibliography_keys = self.extract_bibliography_keys()

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

      if filtered_citations == filtered_bibliography:
          print("- Citations are sorted correctly.")
      else:
          print("- Citations are NOT sorted the same as in the bibliography.")
