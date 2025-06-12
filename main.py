import os
from brd_processor import BRDProcessor
from story_generator import UserStoryGenerator  
from doc_generator import DocumentGenerator

def main():
    """Main processing function"""
    print("🚀 Starting BRD to User Stories conversion...")
    
    # Initialize components
    brd_processor = BRDProcessor()
    story_generator = UserStoryGenerator()
    doc_generator = DocumentGenerator()
    
    # Process BRD
    brd_file = "requirements/requirements.md"
    print(f"📄 Loading BRD: {brd_file}")
    
    try:
        # Step 1: Load and extract requirements
        brd_content = brd_processor.load_brd(brd_file)
        requirements = brd_processor.extract_requirements(brd_content)
        print(f"✅ Extracted {len(requirements['functional_requirements'])} functional requirements")
        
        # Step 2: Generate user stories
        print("🤖 Generating user stories with AI...")
        user_stories = story_generator.generate_stories(requirements)
        print(f"✅ Generated {len(user_stories)} user stories")
        
        # Step 3: Generate document
        output_file = "output/User_Stories_Document.md"
        os.makedirs("output", exist_ok=True)
        
        print("📝 Creating user stories document...")
        doc_generator.generate_user_stories_document(requirements, user_stories, output_file)
        
        # Summary
        total_points = sum(story.get("story_points", 0) for story in user_stories)
        epics = set(story.get("epic", "General") for story in user_stories)
        
        print("\n🎉 Conversion completed successfully!")
        print(f"📊 Summary:")
        print(f"   • {len(user_stories)} user stories generated")
        print(f"   • {total_points} total story points")
        print(f"   • {len(epics)} epics created")
        print(f"   • Document saved: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()