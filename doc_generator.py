from typing import List, Dict
from datetime import datetime

class DocumentGenerator:
    def generate_user_stories_document(self, requirements: Dict, stories: List[Dict], output_path: str):
        """Generate comprehensive user stories document"""
        
        # Group stories by epic
        epics = {}
        for story in stories:
            epic = story.get("epic", "General")
            if epic not in epics:
                epics[epic] = []
            epics[epic].append(story)
        
        # Build document content
        doc_content = self._build_document_header(requirements)
        doc_content += self._build_summary_section(requirements, stories, epics)
        doc_content += self._build_epics_overview(epics)
        doc_content += self._build_detailed_stories(epics)
        doc_content += self._build_requirements_traceability(requirements, stories)
        
        # Save document
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(doc_content)
        
        print(f"📄 User Stories document generated: {output_path}")
    
    def _build_document_header(self, requirements: Dict) -> str:
        """Build document header"""
        project_name = requirements.get("project_name", "Project")
        return f"""# User Stories Document
## {project_name}

**Generated on:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Project Overview](#project-overview)
3. [Epics Overview](#epics-overview)
4. [Detailed User Stories](#detailed-user-stories)
5. [Requirements Traceability](#requirements-traceability)

---

"""
    
    def _build_summary_section(self, requirements: Dict, stories: List[Dict], epics: Dict) -> str:
        """Build executive summary section"""
        total_points = sum(story.get("story_points", 0) for story in stories)
        high_priority = len([s for s in stories if s.get("priority") == "High"])
        
        content = f"""## Executive Summary

This document contains user stories derived from the business requirements for **{requirements.get("project_name", "the project")}**.

### Key Metrics
- **Total User Stories:** {len(stories)}
- **Total Story Points:** {total_points}
- **Number of Epics:** {len(epics)}
- **High Priority Stories:** {high_priority}

### Business Objectives
"""
        
        for objective in requirements.get("business_objectives", []):
            content += f"- {objective}\n"
        
        content += "\n---\n\n"
        return content
    
    def _build_epics_overview(self, epics: Dict) -> str:
        """Build epics overview section"""
        content = "## Epics Overview\n\n"
        
        for epic_name, epic_stories in epics.items():
            total_points = sum(story.get("story_points", 0) for story in epic_stories)
            high_priority = len([s for s in epic_stories if s.get("priority") == "High"])
            
            content += f"### {epic_name}\n"
            content += f"- **Stories:** {len(epic_stories)}\n"
            content += f"- **Story Points:** {total_points}\n"
            content += f"- **High Priority:** {high_priority}\n\n"
        
        content += "---\n\n"
        return content
    
    def _build_detailed_stories(self, epics: Dict) -> str:
        """Build detailed user stories section"""
        content = "## Detailed User Stories\n\n"
        
        for epic_name, epic_stories in epics.items():
            content += f"### Epic: {epic_name}\n\n"
            
            # Sort stories by priority and story points
            sorted_stories = sorted(epic_stories, key=lambda x: (
                {"High": 0, "Medium": 1, "Low": 2}.get(x.get("priority", "Medium"), 1),
                x.get("story_points", 0)
            ))
            
            for story in sorted_stories:
                content += self._format_story_details(story)
            
            content += "---\n\n"
        
        return content
    
    def _format_story_details(self, story: Dict) -> str:
        """Format individual story details"""
        content = f"""#### {story.get('id', 'N/A')}: {story.get('title', 'N/A')}

**User Story:**  
{story.get('user_story', 'N/A')}

**Priority:** {story.get('priority', 'N/A')} | **Story Points:** {story.get('story_points', 'N/A')} | **Source:** {story.get('source_requirement', 'N/A')}

**Acceptance Criteria:**
"""
        
        for i, criteria in enumerate(story.get('acceptance_criteria', []), 1):
            content += f"{i}. {criteria}\n"
        
        content += "\n"
        return content
    
    def _build_requirements_traceability(self, requirements: Dict, stories: List[Dict]) -> str:
        """Build requirements traceability matrix"""
        content = "## Requirements Traceability\n\n"
        content += "| Requirement ID | Requirement Title | User Stories | Story Points |\n"
        content += "|---|---|---|---|\n"
        
        for req in requirements.get("functional_requirements", []):
            req_stories = [s for s in stories if s.get("source_requirement") == req["id"]]
            story_ids = ", ".join([s.get("id", "N/A") for s in req_stories])
            total_points = sum(s.get("story_points", 0) for s in req_stories)
            
            content += f"| {req['id']} | {req['title']} | {story_ids} | {total_points} |\n"
        
        content += "\n---\n\n"
        content += f"*Document generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        
        return content