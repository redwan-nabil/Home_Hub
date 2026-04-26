import os
import shutil
import sys
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

INCOMING_DIR = "incoming"
ROOT_DIR = "."
# The Fallback Array: It will try these one by one until it defeats the 404 error
MODELS_TO_TRY = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-2.0-flash', 'gemini-pro']

def process_scripts():
    if not os.path.exists(INCOMING_DIR):
        print("No incoming directory found. Exiting.")
        return

    for project_folder in os.listdir(INCOMING_DIR):
        project_incoming_path = os.path.join(INCOMING_DIR, project_folder)
        
        if os.path.isdir(project_incoming_path):
            final_project_path = os.path.join(ROOT_DIR, project_folder)
            if not os.path.exists(final_project_path):
                os.makedirs(final_project_path)

            for filename in os.listdir(project_incoming_path):
                filepath = os.path.join(project_incoming_path, filename)
                
                if os.path.isfile(filepath):
                    with open(filepath, "r") as f:
                        new_code = f.read()

                    target_script_path = os.path.join(final_project_path, filename)
                    is_update = os.path.exists(target_script_path)
                    
                    old_code_text = ""
                    update_instructions = "This is a brand new script."
                    
                    if is_update:
                        with open(target_script_path, "r") as old_f:
                            old_code = old_f.read()
                        old_code_text = f"\n\n--- OLD CODE REFERENCE ---\n{old_code}\n"
                        update_instructions = "This is an UPDATE. Compare OLD CODE and NEW CODE. ADD a '🚀 Release Notes' section at the top detailing changes."

                    prompt = f"""
                    You are a Senior DevOps Engineer adding/updating '{filename}' in '{project_folder}'.
                    {update_instructions}
                    Analyze the NEW CODE and write a detailed README. Output ONLY the raw Markdown.
                    --- NEW CODE ---
                    {new_code}
                    {old_code_text}
                    """
                    
                    # --- THE UNBREAKABLE FALLBACK LOOP ---
                    response = None
                    for model_name in MODELS_TO_TRY:
                        try:
                            print(f"🤖 Attempting AI generation with model: {model_name}...")
                            response = client.models.generate_content(
                                model=model_name,
                                contents=prompt
                            )
                            break # If successful, break out of the loop
                        except Exception as e:
                            print(f"⚠️ Model {model_name} failed: {e}")
                    
                    if not response:
                        print(f"❌ FATAL ERROR: All AI models failed for {filename}.")
                        sys.exit(1)
                        
                    readme_content = response.text.strip()
                    if readme_content.startswith("```markdown"):
                        readme_content = readme_content[11:-3].strip()
                    elif readme_content.startswith("```"):
                        readme_content = readme_content[3:-3].strip()
                    
                    base_name = os.path.splitext(filename)[0]
                    md_filename = f"{base_name}.md"
                    
                    shutil.move(filepath, target_script_path)
                    with open(os.path.join(final_project_path, md_filename), "w") as f:
                        f.write(readme_content)
                        
                    print(f"✅ Success! Saved {filename} to /{project_folder}")

            shutil.rmtree(project_incoming_path, ignore_errors=True)

if __name__ == "__main__":
    process_scripts()
