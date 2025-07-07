import os
import json
from pathlib import Path
from datetime import datetime

class BlogManager:
    def __init__(self):
        self.blog_dir = Path("generated_blogs")
        self.metadata_file = self.blog_dir / "blog_metadata.json"
        self.load_metadata()
    
    def load_metadata(self):
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {"posts": []}
    
    def search_posts(self, query):
        query = query.lower()
        return [
            post for post in self.metadata["posts"]
            if query in post["title"].lower() or query in post["prompt"].lower()
        ]
    
    def get_post_content(self, filename):
        filepath = self.blog_dir / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    def delete_post(self, filename):
        filepath = self.blog_dir / filename
        if filepath.exists():
            filepath.unlink()
            self.metadata["posts"] = [
                post for post in self.metadata["posts"] 
                if post["filename"] != filename
            ]
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
            print(f"Deleted: {filename}")
            return True
        else:
            print(f"File not found: {filename}")
            return False
    
    def export_posts_summary(self):
        summary_file = self.blog_dir / "posts_summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("AI BLOG GENERATOR - POSTS SUMMARY\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total Posts: {len(self.metadata['posts'])}\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for i, post in enumerate(self.metadata["posts"], 1):
                date = datetime.fromisoformat(post["generated_date"]).strftime("%Y-%m-%d %H:%M")
                f.write(f"{i}. {post['title']}\n")
                f.write(f"   Prompt: {post['prompt']}\n")
                f.write(f"   Generated: {date}\n")
                f.write(f"   Words: {post['word_count']}\n")
                f.write(f"   File: {post['filename']}\n\n")
        print(f"Summary exported to: {summary_file}")
    
    def run_manager(self):
        print("Blog Manager")
        while True:
            print("\nOptions:")
            print("1. List all posts")
            print("2. Search posts")
            print("3. View post content")
            print("4. Delete post")
            print("5. Export summary")
            print("6. Exit")
            
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                self.list_all_posts()
            elif choice == '2':
                query = input("Enter search term: ").strip()
                results = self.search_posts(query)
                if results:
                    for post in results:
                        print(f"- {post['title']} ({post['filename']})")
                else:
                    print("No matching posts found.")
            elif choice == '3':
                filename = input("Enter filename: ").strip()
                content = self.get_post_content(filename)
                if content:
                    print(content[:500] + "..." if len(content) > 500 else content)
                else:
                    print("File not found.")
            elif choice == '4':
                filename = input("Enter filename to delete: ").strip()
                confirm = input(f"Are you sure you want to delete {filename}? (y/N): ")
                if confirm.lower() == 'y':
                    self.delete_post(filename)
            elif choice == '5':
                self.export_posts_summary()
            elif choice == '6':
                break
            else:
                print("Invalid choice.")
    
    def list_all_posts(self):
        if not self.metadata["posts"]:
            print("No blog posts found.")
            return
        for i, post in enumerate(self.metadata["posts"], 1):
            date = datetime.fromisoformat(post["generated_date"]).strftime("%Y-%m-%d %H:%M")
            print(f"{i}. {post['title']}")
            print(f"   {date} | {post['word_count']} words | {post['filename']}")

def main():
    manager = BlogManager()
    manager.run_manager()

if __name__ == "__main__":
    main()
