# resume_parser/extractor.py
import spacy
from skillNer.skill_extractor_class import SkillExtractor
from skillNer.general_params import SKILL_DB
from spacy.matcher import PhraseMatcher  # Pass this class directly

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize SkillExtractor with defaults
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)

def extract_skills(text):
    """
    Extract skills from text using SkillNer.
    Returns a set of unique skills found.
    """
    annotations = skill_extractor.annotate(text)
    skills_found = set()

    for match in annotations["results"].get("full_matches", []):
        skills_found.add(match.get("doc_node_value", "").strip())
    for match in annotations["results"].get("ngram_scored", []):
        skills_found.add(match.get("doc_node_value", "").strip())

    return list(skills_found)
