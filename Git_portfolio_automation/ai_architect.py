import os
import shutil
import sys
import time
from openai import OpenAI

# Authenticate directly with GitHub's internal AI servers
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key="REDACTED_BY_SYSADMIN"
)

INCOMING_DIR = "incoming"
ROOT_DIR = "."

# GitHub Models available to Pro users
MODELS_TO_TRY = ['gpt-4o', 'gpt-4o-mini']

def call_ai_with_retry(prompt):
    for model in MODELS_TO_TRY:
        for attempt in range(3):
            try:
                print(f"🤖 Attempting AI generation with GitHub Native Model: {model} (Attempt {attempt+1}/3)...")
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a Senior DevOps Engineer. Output ONLY raw Markdown documentation. Do not wrap it in ```markdown codeblocks."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2
                )
                return response.choices[0].message.content
            except Exception as e:
                error_msg = str(e)
                print(f"⚠️ Error with {model}: {error_msg}")
                
                if "429" in error_msg or "RateLimit" in error_msg:
                    sleep_time = 2 ** attempt
                    print(f"⏳ Rate limited. Sleeping for {sleep_time} seconds...")
                    time.sleep(sleep_time)
                    continue
                break
    return None

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
                    You are adding/updating '{filename}' in '{project_folder}'.
                    {update_instructions}
                    Analyze the NEW CODE and write a detailed README. Output ONLY the raw Markdown.
                    --- NEW CODE ---
                    {new_code}
                    {old_code_text}
                    """
                    
                    readme_content = call_ai_with_retry(prompt)
                    base_name = os.path.splitext(filename)[0]
                    md_filename = f"{base_name}.md"
                    
                    if readme_content:
                        readme_content = readme_content.strip()
                        if readme_content.startswith("```markdown"):
                            readme_content = readme_content[11:-3].strip()
                        elif readme_content.startswith("```"):
                            readme_content = readme_content[3:-3].strip()
                    else:
                        print(f"❌ AI blocked. Generating safe fallback template for {filename}...")
                        readme_content = f"# {base_name}\n\nAutomated script deployed to `{project_folder}`.\n\n> **⚠️ System Note:** AI generation failed. Manual documentation required."
                    
                    shutil.move(filepath, target_script_path)
                    with open(os.path.join(final_project_path, md_filename), "w") as f:
                        f.write(readme_content)
                        
                    print(f"✅ Success! Saved {filename} to /{project_folder}")

            shutil.rmtree(project_incoming_path, ignore_errors=True)

if __name__ == "__main__":
    process_scripts()
