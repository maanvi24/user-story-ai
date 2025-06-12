import openai
import os
import json
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class UserStoryGenerator:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
    
    def generate_stories(self, requirements: Dict) -> List[Dict]:
        """Generate user stories from requirements"""
        all_stories = []
        
        for req in requirements.get("functional_requirements", []):
            stories = self._generate_stories_for_requirement(req, requirements)
            all_stories.extend(stories)
        
        return all_stories
    
    def _generate_stories_for_requirement(self, requirement: Dict, context: Dict) -> List[Dict]:
        """Generate user stories for a single requirement"""
        prompt = self._build_prompt(requirement, context)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert product manager and business analyst who creates high-quality user stories from business requirements."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content
            stories = self._parse_ai_response(content, requirement["id"])
            return stories
            
        except Exception as e:
            print(f"Error generating stories for {requirement['id']}: {e}")
            return [self._create_fallback_story(requirement)]
    
    def _build_prompt(self, requirement: Dict, context: Dict) -> str:
        """Build prompt for AI story generation"""
        personas_text = ", ".join([p["name"] for p in context.get("user_personas", [])])
        
        prompt = f"""
Convert this functional requirement into 1-3 detailed user stories:

**Requirement**: {requirement['id']}: {requirement['title']}
**Description**: {requirement['description']}
**Available User Types**: {personas_text}

For each user story, provide:
1. **Title**: Short descriptive title
2. **User Story**: "As a [user type], I want [goal] so that [benefit]"
3. **Acceptance Criteria**: 3-5 specific Given-When-Then scenarios
4. **Priority**: High/Medium/Low based on business impact
5. **Story Points**: Estimate 1-13 (Fibonacci: 1,2,3,5,8,13)
6. **Epic**: Group related functionality (e.g., "User Management", "Task Management")

Format your response as a JSON array of story objects like this:
[
  {{
    "title": "User Registration",
    "user_story": "As a new user, I want to create an account so that I can access the task management system",
    "acceptance_criteria": [
      "Given I am on the registration page, When I enter valid email and password, Then my account should be created",
      "Given I register with an email, When I check my inbox, Then I should receive a verification email"
    ],
    "priority": "High",
    "story_points": 5,
    "epic": "User Management"
  }}
]

Return only the JSON array, no additional text.
"""
        return prompt
    
    def _parse_ai_response(self, response: str, req_id: str) -> List[Dict]:
        """Parse AI response into story objects"""
        try:
            # Clean response
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            
            stories = json.loads(response)
            
            # Add IDs and validate
            for i, story in enumerate(stories):
                story["id"] = f"US-{req_id.replace('FR-', '')}-{i+1:02d}"
                story["source_requirement"] = req_id
                
                # Ensure all required fields exist
                story.setdefault("title", "User Story")
                story.setdefault("user_story", "As a user, I want functionality so that I can achieve my goal")
                story.setdefault("acceptance_criteria", ["Given a condition, When an action occurs, Then an outcome happens"])
                story.setdefault("priority", "Medium")
                story.setdefault("story_points", 3)
                story.setdefault("epic", "General")
            
            return stories
            
        except Exception as e:
            print(f"Error parsing AI response for {req_id}: {e}")
            return [self._create_fallback_story({"id": req_id, "title": "Generated Story"})]
    
    def _create_fallback_story(self, requirement: Dict) -> Dict:
        """Create fallback story when AI fails"""
        return {
            "id": f"US-{requirement['id'].replace('FR-', '')}-01",
            "title": requirement.get("title", "User Story"),
            "user_story": f"As a user, I want {requirement.get('title', 'functionality')} so that I can achieve my goals",
            "acceptance_criteria": [
                "Given the user has access to the system",
                "When they perform the required action", 
                "Then the system should respond appropriately"
            ],
            "priority": "Medium",
            "story_points": 5,
            "epic": "Core Functionality",
            "source_requirement": requirement.get("id", "N/A")
        }