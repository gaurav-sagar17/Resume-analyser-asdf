"""
Resume analyzer with section detection and rule-based scoring.
"""
import re
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class ResumeAnalyzer:
    """Analyzes resumes and provides scores and feedback."""
    
    SECTION_KEYWORDS = {
        'contact': ['email', 'phone', 'address', 'linkedin', 'github', 'contact', 'mobile'],
        'skills': ['skills', 'technical skills', 'competencies', 'proficiencies', 'expertise'],
        'experience': ['experience', 'work experience', 'employment', 'professional experience', 'work history'],
        'education': ['education', 'academic', 'qualifications', 'degree', 'university', 'college'],
        'projects': ['projects', 'project', 'portfolio', 'personal projects'],
        'certifications': ['certifications', 'certificates', 'certification', 'credentials']
    }
    
    SKILL_KEYWORDS = [
        'python', 'java', 'javascript', 'typescript', 'react', 'node', 'sql', 'html', 'css',
        'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'github', 'gitlab',
        'machine learning', 'deep learning', 'data science', 'analytics',
        'agile', 'scrum', 'ci/cd', 'devops', 'microservices', 'api', 'rest',
        'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch',
        'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn'
    ]

    FIELD_KEYWORDS = {
        "software / it": [
            "computer science", "software engineering", "software engineer",
            "full stack", "frontend", "backend", "web development",
            "developer", "programmer", "cloud computing", "devops"
        ],
        "data / ai": [
            "data science", "data scientist", "machine learning", "deep learning",
            "artificial intelligence", "ml engineer", "data engineer",
            "analytics", "business intelligence"
        ],
        "cybersecurity": [
            "cyber security", "cybersecurity", "information security", "infosec",
            "penetration testing", "security analyst", "security engineer"
        ],
        "mechanical engineering": [
            "mechanical engineering", "mechanical engineer", "thermodynamics",
            "cad", "solidworks"
        ],
        "electrical / electronics": [
            "electrical engineering", "electronics engineering",
            "embedded systems", "circuit design", "fpga"
        ],
        "business / management": [
            "business administration", "mba", "management", "project management",
            "product manager", "business analyst"
        ],
        "finance": [
            "finance", "financial analyst", "accounting", "investment",
            "banking", "portfolio management"
        ],
        "marketing": [
            "marketing", "digital marketing", "seo",
            "content marketing", "brand management"
        ],
    }
    
    def __init__(self, text: str):
        self.text = text.lower()
        self.lines = [line.strip() for line in text.split('\n') if line.strip()]
        self.detected_sections: Dict[str, bool] = {}
        self.detected_field: Optional[str] = None
        
    def detect_sections(self) -> Dict[str, bool]:
        sections = {}
        
        for section_name, keywords in self.SECTION_KEYWORDS.items():
            found = False
            for keyword in keywords:
                pattern = rf'^[#\s]*{re.escape(keyword)}[:\s]*$'
                if re.search(pattern, self.text, re.IGNORECASE | re.MULTILINE):
                    found = True
                    break
                if keyword in self.text:
                    found = True
                    break
            sections[section_name] = found
        
        self.detected_sections = sections
        return sections
    
    def analyze_skills(self) -> Tuple[float, List[str], List[str]]:
        score = 0.0
        strengths = []
        weaknesses = []
        
        if not self.detected_sections.get('skills', False):
            weaknesses.append("Skills section not clearly identified")
            return score, strengths, weaknesses
        
        skills_text = self._extract_section_text('skills')
        
        if not skills_text:
            weaknesses.append("Skills section is empty or not found")
            return score, strengths, weaknesses
        
        skill_count = len(re.findall(r'[,\n]', skills_text)) + 1
        if skill_count < 5:
            weaknesses.append(f"Only {skill_count} skills listed - consider adding more")
        elif skill_count >= 10:
            strengths.append(f"Good variety of skills ({skill_count} skills listed)")
            score += 0.5
        else:
            score += 0.3
        
        found_keywords = [kw for kw in self.SKILL_KEYWORDS if kw in skills_text.lower()]
        
        if len(found_keywords) >= 5:
            strengths.append("Strong technical skills with relevant technologies")
            score += 0.8
        elif len(found_keywords) >= 3:
            score += 0.5
        else:
            weaknesses.append("Consider adding more technical skills relevant to your field")
        
        if re.search(r'(programming|language|tool|framework|technology)[:\s]', skills_text, re.IGNORECASE):
            strengths.append("Skills are well-organized")
            score += 0.7
        else:
            score += 0.3
        
        return min(score, 2.0), strengths, weaknesses
    
    def analyze_experience(self) -> Tuple[float, List[str], List[str]]:
        score = 0.0
        strengths = []
        weaknesses = []
        
        if not self.detected_sections.get('experience', False):
            weaknesses.append("Work experience section not clearly identified")
            return score, strengths, weaknesses
        
        experience_text = self._extract_section_text('experience')
        
        if not experience_text:
            weaknesses.append("Experience section is empty")
            return score, strengths, weaknesses
        
        date_pattern = r'\d{4}[-–—]\d{4}|\d{4}\s*[-–—]\s*present|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec'
        date_matches = len(re.findall(date_pattern, experience_text, re.IGNORECASE))
        
        if date_matches >= 2:
            strengths.append(f"Multiple positions listed ({date_matches} positions)")
            score += 1.0
        elif date_matches == 1:
            score += 0.5
        else:
            weaknesses.append("No dates found in experience section")
        
        achievement_patterns = [
            r'\d+%', r'\$\d+', r'\d+\+', 
            r'increased|decreased|improved|reduced|achieved|delivered|managed|led',
            r'\d+\s*(users|customers|projects|team members|employees)'
        ]
        
        achievement_count = sum(len(re.findall(p, experience_text, re.IGNORECASE)) for p in achievement_patterns)
        
        if achievement_count >= 5:
            strengths.append("Strong use of quantifiable achievements")
            score += 1.5
        elif achievement_count >= 2:
            strengths.append("Some measurable achievements present")
            score += 1.0
        else:
            weaknesses.append("Add more quantifiable achievements (numbers, percentages, metrics)")
            score += 0.3
        
        action_verbs = [
            'developed', 'designed', 'implemented', 'created', 'built', 'managed',
            'led', 'improved', 'optimized', 'delivered', 'achieved', 'collaborated'
        ]
        verb_count = sum(1 for verb in action_verbs if verb in experience_text.lower())
        
        if verb_count >= 5:
            strengths.append("Strong use of action verbs")
            score += 0.5
        else:
            score += 0.2
        
        return min(score, 3.0), strengths, weaknesses
    
    def analyze_education(self) -> Tuple[float, List[str], List[str]]:
        score = 0.0
        strengths = []
        weaknesses = []
        
        if not self.detected_sections.get('education', False):
            weaknesses.append("Education section not clearly identified")
            return score, strengths, weaknesses
        
        education_text = self._extract_section_text('education')
        
        if not education_text:
            weaknesses.append("Education section is empty")
            return score, strengths, weaknesses
        
        degree_keywords = ['bachelor', 'master', 'phd', 'doctorate', 'degree', 'diploma', 'certificate']
        has_degree = any(kw in education_text.lower() for kw in degree_keywords)
        
        if has_degree:
            strengths.append("Education credentials clearly listed")
            score += 0.5
        else:
            weaknesses.append("Degree information not clearly stated")
        
        institution_keywords = ['university', 'college', 'institute', 'school']
        has_institution = any(kw in education_text.lower() for kw in institution_keywords)
        
        if has_institution:
            score += 0.3
        else:
            weaknesses.append("Institution name not clearly mentioned")
        
        if re.search(r'\d{4}', education_text):
            score += 0.2
        
        return min(score, 1.0), strengths, weaknesses
    
    def analyze_projects(self) -> Tuple[float, List[str], List[str]]:
        score = 0.0
        strengths = []
        weaknesses = []
        
        if not self.detected_sections.get('projects', False):
            weaknesses.append("Projects section not found - consider adding one")
            return score, strengths, weaknesses
        
        projects_text = self._extract_section_text('projects')
        
        if not projects_text:
            weaknesses.append("Projects section is empty")
            return score, strengths, weaknesses
        
        project_indicators = [
            r'project\s+\d+',
            r'^\s*[-•*]\s+[A-Z]',
            r'^\s*\d+[\.)]\s+[A-Z]',
        ]
        
        project_count = 0
        for pattern in project_indicators:
            matches = len(re.findall(pattern, projects_text, re.MULTILINE | re.IGNORECASE))
            project_count = max(project_count, matches)
        
        if project_count == 0:
            lines = [line for line in projects_text.split('\n') if line.strip()]
            project_count = sum(1 for line in lines if len(line) < 80 and line[0].isupper())
        
        if project_count >= 3:
            strengths.append(f"Good number of projects listed ({project_count})")
            score += 1.0
        elif project_count >= 2:
            strengths.append("At least 2 projects listed")
            score += 0.8
        elif project_count == 1:
            weaknesses.append("Only 1 project listed - consider adding more")
            score += 0.4
        else:
            weaknesses.append("No clear projects identified")
            return score, strengths, weaknesses
        
        tech_mentions = sum(1 for keyword in self.SKILL_KEYWORDS[:10] if keyword in projects_text.lower())
        
        if tech_mentions >= 3:
            strengths.append("Projects include relevant technical details")
            score += 0.7
        elif tech_mentions >= 1:
            score += 0.4
        else:
            weaknesses.append("Add more technical details to project descriptions")
        
        if re.search(r'(github|gitlab|demo|link|url)', projects_text, re.IGNORECASE):
            strengths.append("Projects include links or references")
            score += 0.3
        
        return min(score, 2.0), strengths, weaknesses
    
    def analyze_formatting(self) -> Tuple[float, List[str], List[str]]:
        score = 0.0
        strengths = []
        weaknesses = []
        
        bullet_patterns = [r'[-•*]\s+', r'^\s*[-•*]']
        has_bullets = any(re.search(pattern, self.text, re.MULTILINE) for pattern in bullet_patterns)
        
        if has_bullets:
            strengths.append("Uses bullet points for readability")
            score += 0.5
        else:
            weaknesses.append("Consider using bullet points for better readability")
        
        word_count = len(self.text.split())
        estimated_pages = word_count / 500
        
        if estimated_pages <= 2:
            strengths.append(f"Appropriate length (~{estimated_pages:.1f} pages)")
            score += 0.7
        elif estimated_pages <= 3:
            score += 0.4
            weaknesses.append(f"Resume is a bit long (~{estimated_pages:.1f} pages) - consider condensing")
        else:
            weaknesses.append(f"Resume is too long (~{estimated_pages:.1f} pages) - aim for 1-2 pages")
        
        section_headers = sum(1 for section in self.detected_sections.values() if section)
        if section_headers >= 4:
            strengths.append("Well-organized with clear sections")
            score += 0.5
        else:
            score += 0.2
        
        contact_patterns = [
            r'[\w\.-]+@[\w\.-]+\.\w+',
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        ]
        has_contact = any(re.search(pattern, self.text, re.IGNORECASE) for pattern in contact_patterns)
        
        if has_contact:
            strengths.append("Contact information present")
            score += 0.3
        else:
            weaknesses.append("Contact information not clearly visible")
        
        return min(score, 2.0), strengths, weaknesses
    
    def analyze_ats_readiness(self) -> Tuple[int, List[str], List[str]]:
        score = 50
        strengths = []
        weaknesses = []
        text = self.text

        core_sections = ["skills", "experience", "education"]
        core_present = sum(1 for s in core_sections if self.detected_sections.get(s))
        
        if core_present == len(core_sections):
            score += 15
            strengths.append("Core sections are clearly present")
        elif core_present >= 2:
            score += 8
            strengths.append("Most core sections are present")
        else:
            weaknesses.append("Missing one or more core sections that ATS tools expect")

        has_email = bool(re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text))
        has_phone = bool(re.search(r"\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text))

        if has_email and has_phone:
            score += 10
            strengths.append("Contact info is easy to parse")
        elif has_email or has_phone:
            score += 4
            weaknesses.append("Consider including both email and phone")
        else:
            weaknesses.append("ATS may struggle to find your contact info")

        bullet_patterns = [r"^\s*[-•*]\s+", r"^\s*\d+[\.)]\s+"]
        has_bullets = any(re.search(p, text, re.MULTILINE) for p in bullet_patterns)

        avg_line_len = sum(len(l) for l in self.lines) / len(self.lines) if self.lines else 0

        if has_bullets:
            score += 10
            strengths.append("Bullets improve ATS scanability")
        else:
            weaknesses.append("Add bullet points to improve ATS readability")

        if avg_line_len > 140:
            weaknesses.append("Some lines are very long; shorten for ATS readability")
            score -= 5

        word_count = len(text.split())
        estimated_pages = word_count / 500

        if estimated_pages <= 2:
            score += 10
            strengths.append("ATS-friendly length (1–2 pages)")
        elif estimated_pages <= 3:
            score += 2
            weaknesses.append("Resume slightly long")
        else:
            score -= 8
            weaknesses.append("Resume too long; shorten to 1–2 pages")

        many_double_spaces = len(re.findall(r" {3,}", text)) > 10
        many_pipes = text.count("|") > 15

        if many_double_spaces or many_pipes:
            score -= 8
            weaknesses.append("Layout may use tables or columns; ATS prefers simple layouts")

        non_ascii_chars = [ch for ch in text if ord(ch) > 127]
        if len(non_ascii_chars) > 30:
            score -= 7
            weaknesses.append("Too many special symbols; ATS prefers simple characters")

        score = max(0, min(100, score))
        return score, strengths, weaknesses
    
    def _extract_section_text(self, section_name: str) -> str:
        keywords = self.SECTION_KEYWORDS.get(section_name, [])
        if not keywords:
            return ""
        
        section_start = -1
        for keyword in keywords:
            pattern = rf'^[#\s]*{re.escape(keyword)}[:\s]*$'
            match = re.search(pattern, self.text, re.IGNORECASE | re.MULTILINE)
            if match:
                section_start = match.start()
                break
        
        if section_start == -1:
            for keyword in keywords:
                if keyword in self.text:
                    idx = self.text.find(keyword)
                    if idx != -1:
                        section_start = idx
                        break
        
        if section_start == -1:
            return ""
        
        remaining_text = self.text[section_start:]
        
        next_section = len(remaining_text)
        for other_section, other_keywords in self.SECTION_KEYWORDS.items():
            if other_section == section_name:
                continue
            for keyword in other_keywords:
                pattern = rf'^[#\s]*{re.escape(keyword)}[:\s]*$'
                match = re.search(pattern, remaining_text, re.IGNORECASE | re.MULTILINE)
                if match and match.start() < next_section:
                    next_section = match.start()
        
        return remaining_text[:next_section]

    def _get_field_keywords(self, field_name: str) -> List[str]:
        return self.FIELD_KEYWORDS.get(field_name, [])

    def detect_field(self) -> Optional[str]:
        relevant_text_parts = []
        for section in ["education", "skills", "projects", "experience"]:
            relevant_text_parts.append(self._extract_section_text(section))

        combined_text = "\n".join([t for t in relevant_text_parts if t]) or self.text
        combined_text_lower = combined_text.lower()

        best_field = None
        best_score = 0

        for field_name, keywords in self.FIELD_KEYWORDS.items():
            hits = sum(1 for kw in keywords if kw in combined_text_lower)
            if hits > best_score:
                best_score = hits
                best_field = field_name

        if best_field and best_score >= 2:
            self.detected_field = best_field
        else:
            self.detected_field = None

        return self.detected_field
    
    def analyze(self) -> Dict:
        self.detect_sections()
        self.detect_field()
        
        skills_score, skills_strengths, skills_weaknesses = self.analyze_skills()
        exp_score, exp_strengths, exp_weaknesses = self.analyze_experience()
        edu_score, edu_strengths, edu_weaknesses = self.analyze_education()
        proj_score, proj_strengths, proj_weaknesses = self.analyze_projects()
        fmt_score, fmt_strengths, fmt_weaknesses = self.analyze_formatting()
        ats_score, ats_strengths, ats_weaknesses = self.analyze_ats_readiness()
        
        total_score = skills_score + exp_score + edu_score + proj_score + fmt_score
        
        strengths = skills_strengths + exp_strengths + edu_strengths + proj_strengths + fmt_strengths + ats_strengths
        weaknesses = skills_weaknesses + exp_weaknesses + edu_weaknesses + proj_weaknesses + fmt_weaknesses + ats_weaknesses

        if self.detected_field:
            strengths.append(f"Primary field detected as: {self.detected_field.title()}")
        else:
            weaknesses.append("Could not clearly detect your primary field of study or work.")
        
        return {
            "score": round(total_score, 1),
            "sections": {
                "skills": round(skills_score, 1),
                "experience": round(exp_score, 1),
                "education": round(edu_score, 1),
                "projects": round(proj_score, 1),
                "formatting": round(fmt_score, 1),
            },
            "strengths": strengths,
            "weaknesses": weaknesses,
            "detected_sections": self.detected_sections,
            "ats_readiness": ats_score,
            "field": self.detected_field,
        }
