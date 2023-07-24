from pybtex.database import parse_file, BibliographyData

def read_journal_abbreviations(filename):
    """Read journal abbreviations from a file and return them as a dictionary."""
    abbreviations = {}
    with open(filename, 'r') as file:
        for line in file:
            full_name, abbreviation = line.strip().split(',')
            abbreviations[full_name.strip()] = abbreviation.strip()
    return abbreviations

def add_journal_abbreviation(filename, full, abbreviation):
  with open(filename, 'a') as file:
    file.write(full + ", "+ abbreviation + "\n")
  return   
   
def convert_to_thebibliography(bib_file, abbr_file):
    journal_abbreviations = read_journal_abbreviations(abbr_file)
    bib_data = parse_file(bib_file)
    print(bib_data)
    output = "\\begin{thebibliography}{99}\n"
    for entry_key in bib_data.entries:
        entry = bib_data.entries[entry_key]
        output += f"\\bibitem{{{entry_key.strip()}}}\n"
        if entry.type == "article":

          title = entry.fields['title'] 
          author = ""
          for xx in entry.persons['author']:
            for i in xx.first_names:
              author += i + " "
            for i in xx.middle_names:
              author += i + " "
            for i in xx.last_names:
              author += i
            author += ", " 
          journal = entry.fields['journaltitle']
          # Replace journal name with abbreviation if available
          if journal in journal_abbreviations:
              journal = journal_abbreviations[journal]
          else:
            print("Abbreviation for ``" + journal + "`` not found.")
            abbreviation = input("\n\tEnter abbreviation : ")
            add_journal_abbreviation(abbr_file, journal, abbreviation)

          output += f"{author} {journal} "

          try:
            volume = entry.fields['volume']
            output += f"\\textbf{{{volume}}}, "
          except:
            print("No volume!!!")

          # try:
          #   number = entry.fields['number']
          #   output += f"{number} "
          # except:
          #   print("No number!!!")
          
          try:
            pages = entry.fields['pages']
            output += f"{pages} "
          except:
            print("No pages!!!")
          date = entry.fields['date']
          output += f" ({date})."
          output += "\n\n"
        elif entry.type == "incollection":
           print("INCOLLECTION!!!")
           output += entry_key.strip()
           output += "\n\n"
        elif entry.type == "book":
          print("BOOK!!!") 

    output += "\end{thebibliography}"
    return output

if __name__ == "__main__":
    # Replace 'journal_abbreviations.txt' with the actual file containing journal abbreviations

    output_file = "thebibliography.tex"
    # Replace 'input.bib' with the actual name of your .bib file
    converted_text = convert_to_thebibliography('collision.bib', 'journal_abbreviations.txt')

    # Print or save 'converted_text' to a file to get the \thebibliography formatted output
    # print(converted_text)

    try:
        with open(output_file, 'w', encoding='utf-8') as output:
          output.write(converted_text)
    except IOError:
        print(f"Error: Unable to write to '{output_file}'.")