import os
import re
import json
from datetime import datetime
from pathlib import Path
import google.generativeai as genai

class BlogGenerator:
    def __init__(self):
        api_key = 'YOUR_GEMINI_API_KEY'
        if not api_key:
            return
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-1.5-flash')
        self.blog_dir = Path("generated_blogs")
        self.blog_dir.mkdir(exist_ok=True)
        self.metadata_file = self.blog_dir / "blog_metadata.json"
        self.load_metadata()
    
    def load_metadata(self):
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {"posts": []}
    
    def save_metadata(self):
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
    
    def sanitize_filename(self, title):
        filename = re.sub(r'[^\w\s-]', '', title)
        filename = re.sub(r'[-\s]+', '-', filename)
        return filename.lower().strip('-')
    
    def generate_blog_content(self, title_prompt):
        prompt = f"""
        Write a comprehensive, engaging blog post about: "{title_prompt}"

        Structure it with:
        1. A clear title
        2. Introduction
        3. Main content with subheadings
        4. Examples or insights
        5. Conclusion
        6. SEO-friendly content

        Minimum length: 800-1200 words.
        """
        try:
            print(f"Generating blog content for: '{title_prompt}'...")
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating content: {str(e)}")
            return None
    
    def save_blog_post(self, title_prompt, content):
        if not content:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = self.sanitize_filename(title_prompt)
        filename = f"{timestamp}_{safe_title}.md"
        filepath = self.blog_dir / filename
        
        lines = content.strip().split('\n')
        generated_title = lines[0].strip('# ').strip() if lines else title_prompt
        
        markdown_content = f"""---
title: "{generated_title}"
prompt: "{title_prompt}"
generated_date: "{datetime.now().isoformat()}"
filename: "{filename}"
---

{content}
"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            post_metadata = {
                "title": generated_title,
                "prompt": title_prompt,
                "filename": filename,
                "filepath": str(filepath),
                "generated_date": datetime.now().isoformat(),
                "word_count": len(content.split())
            }
            self.metadata["posts"].append(post_metadata)
            self.save_metadata()
            print(f"Blog post saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving blog post: {str(e)}")
            return None
    
    def list_generated_posts(self):
        if not self.metadata["posts"]:
            print("No blog posts generated yet.")
            return
        
        for i, post in enumerate(self.metadata["posts"], 1):
            date = datetime.fromisoformat(post["generated_date"]).strftime("%Y-%m-%d %H:%M")
            print(f"{i}. {post['title']} ({post['word_count']} words) - {date} - {post['filename']}")
    
    def run_interactive_mode(self):
        print("AI Blog Generator")
        
        while True:
            print("\nOptions:")
            print("1. Generate new blog post")
            print("2. List generated posts")
            print("3. Exit")
            
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == '1':
                title_prompt = input("Enter blog title or topic: ").strip()
                if title_prompt:
                    content = self.generate_blog_content(title_prompt)
                    if content:
                        self.save_blog_post(title_prompt, content)
                    else:
                        print("Failed to generate content.")
                else:
                    print("Please enter a valid title or topic.")
            elif choice == '2':
                self.list_generated_posts()
            elif choice == '3':
                break
            else:
                print("Invalid choice. Enter 1, 2, or 3.")

def main():
    generator = BlogGenerator()
    if not hasattr(generator, 'model'):
        return
    generator.run_interactive_mode()

if __name__ == "__main__":
    main()
