import re
import os
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

class BRDProcessor:
    def __init__(self):
        pass
    
    def load_brd(self, file_path: str) -> str:
        """Load BRD content from file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def extract_requirements(self, brd_content: str) -> Dict:
        """Extract structured requirements from BRD"""
        requirements = {
            "project_name": self._extract_project_name(brd_content),
            "business_objectives": self._extract_business_objectives(brd_content),
            "functional_requirements": self._extract_functional_requirements(brd_content),
            "user_personas": self._extract_user_personas(brd_content),
            "business_rules": self._extract_business_rules(brd_content)
        }
        return requirements
    
    def _extract_project_name(self, content: str) -> str:
        """Extract project name from BRD title"""
        match = re.search(r'# Business Requirements Document: (.+)', content)
        return match.group(1).strip() if match else "Project"
    
    def _extract_business_objectives(self, content: str) -> List[str]:
        """Extract business objectives"""
        objectives = []
        # Look for bullet points under Business Objectives
        obj_section = re.search(r'### Business Objectives\n(.*?)(?=\n##|\n###|\Z)', content, re.DOTALL)
        if obj_section:
            lines = obj_section.group(1).strip().split('\n')
            for line in lines:
                if line.strip().startswith('-'):
                    objectives.append(line.strip()[1:].strip())
        return objectives
    
    def _extract_functional_requirements(self, content: str) -> List[Dict]:
        """Extract functional requirements"""
        requirements = []
        # Pattern to match FR sections
        fr_pattern = r'### (FR-\d+): (.+?)\n(.*?)(?=\n### FR-|\n## |\Z)'
        matches = re.findall(fr_pattern, content, re.DOTALL)
        
        for match in matches:
            req_id, title, description = match
            
            # Extract details if present
            details = []
            detail_match = re.search(r'\*\*Details:\*\*\n(.*?)(?=\n\*\*|\Z)', description, re.DOTALL)
            if detail_match:
                detail_lines = detail_match.group(1).strip().split('\n')
                for line in detail_lines:
                    if line.strip().startswith('-'):
                        details.append(line.strip()[1:].strip())
            
            requirements.append({
                "id": req_id.strip(),
                "title": title.strip(),
                "description": description.strip(),
                "details": details
            })
        
        return requirements
    
    def _extract_user_personas(self, content: str) -> List[Dict]:
        """Extract user personas"""
        personas = []
        persona_section = re.search(r'### Primary Users\n(.*?)(?=\n##|\n###|\Z)', content, re.DOTALL)
        if persona_section:
            lines = persona_section.group(1).strip().split('\n')
            for line in lines:
                if line.strip().startswith('- **'):
                    match = re.match(r'- \*\*(.+?)\*\*: (.+)', line.strip())
                    if match:
                        personas.append({
                            "name": match.group(1),
                            "description": match.group(2)
                        })
        return personas
    
    def _extract_business_rules(self, content: str) -> List[Dict]:
        """Extract business rules"""
        rules = []
        # Pattern to match BR sections
        br_pattern = r'### (BR-\d+): (.+?)\n(.*?)(?=\n### BR-|\n## |\Z)'
        matches = re.findall(br_pattern, content, re.DOTALL)
        
        for match in matches:
            rule_id, title, description = match
            rules.append({
                "id": rule_id.strip(),
                "title": title.strip(),
                "description": description.strip()
            })
        
        return rules