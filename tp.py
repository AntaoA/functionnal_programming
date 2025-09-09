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

def analyze_basic_scientists(scientists: List[Scientist]) -> Dict:
    """
    Use map, filter, reduce to analyze scientists.
    Return a dictionary with:
    - 'nobel_winners': filtered scientists with Nobel prizes
    - 'total_birth_years': sum of all birth years
    - 'avg_birth_year': average birth year
    - 'scientist_names': list of all scientist names (uppercase)

    Use lambda functions where appropriate.
    """
    dict_processors = create_scientist_processors()
    dict_analysis = {
        'nobel_winners': list(filter(dict_processors['is_nobel_winner'], scientists)),
        'total_birth_years': reduce(lambda acc, scientist: acc + scientist.birth_year, scientists, 0),
        'avg_birth_year': reduce(lambda acc, scientist: acc + scientist.birth_year, scientists, 0) / len(scientists) if scientists else 0,
        'scientist_names': list(map(lambda scientist: scientist.name.upper(), scientists))
    }

    return dict_analysis


def get_field_statistics(scientists: List[Scientist]) -> Dict[str, Dict]:
    """
    Create statistics per field using functional programming.
    Return dict where keys are fields and values are dicts with:
    - 'scientist_count': number of scientists in field
    - 'nobel_count': number of Nobel winners in field
    - 'avg_birth_year': average birth year in field
    - 'nobel_percentage': percentage who won Nobel prizes

    Use map, filter, reduce paradigm.
    """
    all_fields = set(map(lambda scientist: scientist.field, scientists))
    dict_field_stats = {}
    for field in all_fields:
        scientists_in_field = list(filter(lambda scientist: scientist.field == field, scientists))
        dict_analysis_filed = analyze_basic_scientists(scientists_in_field)
        
        dict_field_stats[field] = {
            'scientist_count': len(scientists_in_field),
            'nobel_count': len(dict_analysis_filed['nobel_winners']),
            'avg_birth_year': dict_analysis_filed['avg_birth_year'],
            'nobel_percentage': (len(dict_analysis_filed['nobel_winners']) / len(scientists_in_field) * 100) if scientists_in_field else 0
        }
    return dict_field_stats



def create_research_analyzer(impact_threshold: float):
    """
    Create a research analyzer using inner functions and closures.
    Returns a function that can analyze scientists and publications.
    """

    def analyze_research_database(scientists: List[Scientist], publications: List[Publication]) -> Database:
        """
        Inner function that analyzes scientists and publications to create database.
        Should categorize research and identify patterns.
        """

        def calculate_field_research(scientists: List[Scientist]) -> List[Research]:
            """
            Nested inner function to calculate research metrics per field.
            Group scientists by field and calculate:
            - Total scientists in field
            - Average birth year
            - Number of Nobel winners
            - High-impact publications in field
            """
            # TODO: Implement research calculation
            dict_field_stats = get_field_statistics(scientists)
            list_research = []

            for field, stats in dict_field_stats.items():

                top_publications = filter_high_impact_research(list(filter(lambda pub: any(scientist.name == pub.author and scientist.field == field for scientist in scientists), publications)))
                research = Research(
                    field=field,
                    total_scientists=stats['scientist_count'],
                    avg_birth_year=stats['avg_birth_year'],
                    nobel_winners=stats['nobel_count'],
                    top_publications=top_publications
                )
                list_research.append(research)
            return list_research


           


        def filter_high_impact_research(publications: List[Publication]) -> List[Publication]:
            """
            Nested inner function using the closure's impact_threshold.
            Filter publications that exceed the impact threshold.
            Score = citations * field impact score
            """
            # TODO: Use impact_threshold from closure
            list_high_impact = []
            for pub in publications:
                for scientist in scientists:
                    if pub.author == scientist.name:
                        field_score = research_impact_scores.get(scientist.field, 0)
                        impact_score = pub.citations * field_score
                        if impact_score >= impact_threshold:
                            list_high_impact.append(pub)
            return list_high_impact
        
        
            
        # TODO: Use inner functions to build database
        research_areas = calculate_field_research(scientists)
        high_impact_publications = filter_high_impact_research(publications)
        database = Database(
            scientists=scientists,
            publications=high_impact_publications,
            research_areas=research_areas
        )
        return database
        
    return analyze_research_database


def create_scientist_filter_factory():
    """
    Create a factory function that returns customized filter functions.
    Uses closures to create specialized filters.
    """

    def create_era_filter(start_year: int, end_year: int):
        """Inner function that creates an era-based filter"""
        # TODO: Return a function that filters scientists by birth year range
        return lambda scientist: start_year <= scientist.birth_year <= end_year

    def create_nationality_filter(nationalities: frozenset):
        """Inner function that creates a nationality-based filter"""
        # TODO: Return a function that filters scientists by nationalities
        return lambda scientist: scientist.nationality in nationalities

    def create_field_group_filter(field_groups: Dict[str, frozenset]):
        """Inner function that creates field group filters"""
        # Example: {'STEM': frozenset(['Physics', 'Chemistry', 'Biology','Mathematics'])}
        # TODO: Return a function that filters by field groups
        return lambda scientist: any(scientist.field in fields for fields in field_groups.values())

    return {
    'era_filter': create_era_filter,
    'nationality_filter': create_nationality_filter,
    'field_group_filter': create_field_group_filter
    }





def create_scientific_report_generator():
    """
    Create a report generator that maintains immutability while
    building complex scientific analysis structures.
    """

    ScientificReport = namedtuple('ScientificReport', [
        'executive_summary', 'field_analysis', 'diversity_metrics', 'collaboration_networks', 'recommendations', 'future_predictions'
    ])

    def generate_comprehensive_scientific_report(scientists: List[Scientist], publications: List[Publication]) -> ScientificReport:
        """
        Generate a comprehensive scientific report using only immutable
        operations.
        No variables should be modified after creation.
        """

        def create_executive_summary(scientists: List[Scientist]) -> Dict:
            """Create executive summary using map-filter-reduce only"""
            # TODO: Create high-level statistics
            # Include: total scientists, fields covered, Nobel winners, time span, etc.
            dict_summary = {
                'total_scientists': len(scientists),
                'fields_covered': list(set(map(lambda s: s.field, scientists))),
                'nobel_winners': len(list(filter(lambda s: s.nobel_prize is not None, scientists))),
                'time_span': (min(map(lambda s: s.birth_year, scientists)), max(map(lambda s: s.birth_year, scientists))) if scientists else (None, None)
            }
            return dict_summary

        def create_field_analysis(scientists: List[Scientist], publications: List[Publication]) -> Dict[str, Dict]:
            """Create detailed field analysis using functional methods"""
            # TODO: Analyze each field comprehensively
            # Include: scientist count, publication impact, Nobel rate, etc.
            return get_field_statistics(scientists)

        def create_collaboration_networks(publications: List[Publication]) -> Dict:
            """Create collaboration network analysis using pure functions"""
            # TODO: Map collaboration patterns
            pass

        def create_diversity_analysis(scientists: List[Scientist]) -> Dict:
            """Create diversity analysis using functional programming"""
            # TODO: Analyze representation across dimensions
            pass

    return generate_comprehensive_scientific_report
    
def create_scientific_ranking_system():
    """
    Create a ranking system for scientists using functional programming.
    """

    ScientistRanking = namedtuple('ScientistRanking', ['scientist', 'score', 'rank', 'category'])

    def rank_scientists_by_impact(scientists: List[Scientist], publications: List[Publication]) -> List[ScientistRanking]:
        """
        Create scientist rankings using only functional operations.
        """

        def calculate_base_score(scientist: Scientist) -> float:
            """Calculate base impact score using functional approach"""
            # TODO: Score based on Nobel prizes, field impact, era, etc.
            score = 0
            if scientist.nobel_prize:
                score += 1000
            field_score = research_impact_scores.get(scientist.field, 0)
            score += field_score * 10
            current_year = datetime.now().year
            age = current_year - scientist.birth_year
            score += max(0, (150 - age))
            

        def categorize_scientist(scientist: Scientist, score: float) -> str:
            """Categorize scientist based on score"""
            # TODO: Create categories like 'Legendary', 'Pioneering', 'Influential', etc.
            if score >= 1200:
                return 'Legendary'
            elif score >= 800:
                return 'Pioneering'
            elif score >= 400:
                return 'Influential'
            else:
                return 'Notable'

        # TODO: Combine all scoring functions to create final rankings
        ranked_scientists = sorted(
            [
                ScientistRanking(
                    scientist=scientist,
                    score=calculate_base_score(scientist),
                    rank=0,  # Placeholder, will set later
                    category=categorize_scientist(scientist, calculate_base_score(scientist))
                )
                for scientist in scientists
            ],
            key=lambda sr: sr.score,
            reverse=True
        )
        
        for idx, sr in enumerate(ranked_scientists):
            ranked_scientists[idx] = sr._replace(rank=idx + 1)

        return ranked_scientists

    return rank_scientists_by_impact


if __name__ == "__main__":

    processors = create_scientist_processors()

    for scientist in sample_scientists:
        print(f"Scientist: {scientist.name}")
        print(f"  Is Nobel Winner: {processors['is_nobel_winner'](scientist)}")
        print(f"  Is Female: {processors['is_female'](scientist)}")
        print(f"  Field Prefix: {processors['field_prefix'](scientist)}")
        print(f"  Formatted: {processors['format_scientist'](scientist)}")

    analysis = analyze_basic_scientists(sample_scientists)

    print("\nAnalysis of Scientists:")
    print(f"  Nobel Winners: {[s.name for s in analysis['nobel_winners']]}")
    print(f"  Total Birth Years: {analysis['total_birth_years']}")
    print(f"  Average Birth Year: {analysis['avg_birth_year']}")
    print(f"  Scientist Names: {analysis['scientist_names']}")
    
    field_stats = get_field_statistics(sample_scientists)
    
    print("\nField Statistics:")
    for field, stats in field_stats.items():
        print(f"  Field: {field}")
        print(f"    Scientist Count: {stats['scientist_count']}")
        print(f"    Nobel Count: {stats['nobel_count']}")
        print(f"    Average Birth Year: {stats['avg_birth_year']}")
        print(f"    Nobel Percentage: {stats['nobel_percentage']}%")    
        
    research_analyzer = create_research_analyzer(impact_threshold=25000)
    database = research_analyzer(sample_scientists, sample_publications)
    print("\nResearch Database:")
    print(f"  Total Scientists: {len(database.scientists)}")
    print(f"  High Impact Publications: {[pub.title for pub in database.publications]}")
    for research in database.research_areas:
        print(f"  Research Field: {research.field}")
        print(f"    Total Scientists: {research.total_scientists}")
        print(f"    Average Birth Year: {research.avg_birth_year}")
        print(f"    Nobel Winners: {research.nobel_winners}")
        print(f"    Top Publications: {[pub.title for pub in research.top_publications]}")
        
    filter_factory = create_scientist_filter_factory()
    era_filter = filter_factory['era_filter'](1900, 1915)
    nationality_filter = filter_factory['nationality_filter'](frozenset(['American', 'British']))
    field_group_filter = filter_factory['field_group_filter']({'STEM': frozenset(['Physics', 'Mathematics'])})

    print("\nFiltered Scientists (Born 1900-1915):")
    for scientist in filter(era_filter, sample_scientists):
        print(f"  {scientist.name} ({scientist.birth_year})")
    print("\nFiltered Scientists (American or British):")
    for scientist in filter(nationality_filter, sample_scientists):
        print(f"  {scientist.name} ({scientist.nationality})")
    print("\nFiltered Scientists (Mathematics or Physics):")
    for scientist in filter(field_group_filter, sample_scientists):
        print(f"  {scientist.name} ({scientist.field})")