from collections import namedtuple
from functools import reduce
from typing import List, Tuple, Dict, Callable
import copy
from datetime import datetime

# Define immutable data structures
Scientist = namedtuple('Scientist', ['name', 'field', 'birth_year', 'nobel_prize', 'nationality'])

Publication = namedtuple('Publication', ['title', 'author', 'year', 'citations', 'journal'])

Research = namedtuple('Research', ['field', 'total_scientists', 'avg_birth_year', 'nobel_winners', 'top_publications'])

Database = namedtuple('Database', ['scientists', 'publications', 'research_areas'])

# Sample data to work with
sample_scientists = [
    Scientist('Marie Curie', 'Physics', 1867, 'Physics 1903, Chemistry 1911', 'French'),
    Scientist('Albert Einstein', 'Physics', 1879, 'Physics 1921', 'German'),
    Scientist('Niels Bohr', 'Physics', 1885, 'Physics 1922', 'Danish'),
    Scientist('Linus Pauling', 'Chemistry', 1901, 'Chemistry 1954, Peace 1962', 'American'),
    Scientist('Barbara McClintock', 'Biology', 1902, 'Physiology/Medicine 1983', 'American'),
    Scientist('Dorothy Hodgkin', 'Chemistry', 1910, 'Chemistry 1964', 'British'),
    Scientist('Rosalind Franklin', 'Chemistry', 1920, None, 'British'),
    Scientist('James Watson', 'Biology', 1928, 'Physiology/Medicine 1962', 'American'),
    Scientist('Francis Crick', 'Biology', 1916, 'Physiology/Medicine 1962', 'British'),
    Scientist('Chien-Shiung Wu', 'Physics', 1912, None, 'Chinese'),
    Scientist('Rita Levi-Montalcini', 'Biology', 1909, 'Physiology/Medicine 1986', 'Italian'),
    Scientist('Katherine Johnson', 'Mathematics', 1918, None, 'American'),
]

sample_publications = [
    Publication('On the Constitution of Atoms and Molecules', 'Niels Bohr', 1913, 2500, 'Philosophical Magazine'),
    Publication('The Structure of DNA', 'James Watson', 1953, 8000, 'Nature'),
    Publication('X-ray Studies of DNA', 'Rosalind Franklin', 1953, 1200, 'Acta Crystallographica'),
    Publication('The Nature of the Chemical Bond', 'Linus Pauling', 1939, 5000, 'Journal of American Chemical Society'),
    Publication('Radioactive Substances', 'Marie Curie', 1904, 3000, 'Annales de Physique'),
    Publication('Genetic Control Systems', 'Barbara McClintock', 1961, 1500, 'Cold Spring Harbor Symposia'),
    Publication('Protein Crystallography', 'Dorothy Hodgkin', 1935, 2200, 'Nature'),
    Publication('Nerve Growth Factor', 'Rita Levi-Montalcini', 1960, 1800, 'Science'),
]

research_impact_scores = {
    'Physics': 9.2,
    'Chemistry': 8.8,
    'Biology': 9.0,
    'Mathematics': 8.5
}




def create_scientist_processors():
    """
    Return a dictionary of lambda functions for processing scientists:
    - 'is_nobel_winner': lambda that returns True if scientist has Nobel
    prize
    - 'is_female': lambda that returns True if scientist is likely female
    (basic name check)
    - 'field_prefix': lambda that returns first 4 letters of field
    - 'format_scientist': lambda that formats as "NAME (FIELD, BIRTH_YEAR)"
    """
    
    # TODO: Create and return dictionary of lambda functions
    # Hint: For female names, check if name starts with common female names
    female_names = {'Marie', 'Barbara', 'Dorothy', 'Rosalind', 'ChienShiung', 'Rita', 'Katherine'}

    dict_processors = {
        'is_nobel_winner': lambda scientist: scientist.nobel_prize is not None,
        'is_female': lambda scientist: scientist.name.split()[0] in female_names,
        'field_prefix': lambda scientist: scientist.field[:4],
        'format_scientist': lambda scientist: f"{scientist.name} ({scientist.field}, {scientist.birth_year})"
    }

    return dict_processors



if __name__ == "__main__":
    processors = create_scientist_processors()
    for scientist in sample_scientists:
        print(f"Scientist: {scientist.name}")
        print(f"  Is Nobel Winner: {processors['is_nobel_winner'](scientist)}")
        print(f"  Is Female: {processors['is_female'](scientist)}")
        print(f"  Field Prefix: {processors['field_prefix'](scientist)}")
        print(f"  Formatted: {processors['format_scientist'](scientist)}")