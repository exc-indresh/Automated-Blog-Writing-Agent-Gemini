import os
from blog_generator import BlogGenerator

def generate_multiple_blogs():

    blog_topics = [
        "The Future of Artificial Intelligence in Healthcare",
        "10 Essential Python Tips for Beginners",
        "Sustainable Living: Small Changes, Big Impact",
        "The Rise of Remote Work: Challenges and Opportunities",
        "Cybersecurity Best Practices for Small Businesses",
        "The Psychology of Productivity: Science-Backed Strategies",
        "Climate Change and Renewable Energy Solutions",
        "Digital Marketing Trends for 2024",
        "The Art of Effective Communication in the Workplace",
        "Mindfulness and Mental Health in the Digital Age"
    ]
    
    generator = BlogGenerator()
    
    if not hasattr(generator, 'model'):
        return
    
    print(f"Starting batch generation of {len(blog_topics)} blog posts...")
    print("-" * 60)
    
    successful_posts = 0
    failed_posts = 0
    
    for i, topic in enumerate(blog_topics, 1):
        print(f"\n[{i}/{len(blog_topics)}] Processing: {topic}")
        
        content = generator.generate_blog_content(topic)
        if content:
            filepath = generator.save_blog_post(topic, content)
            if filepath:
                successful_posts += 1
            else:
                failed_posts += 1
        else:
            failed_posts += 1
            print(f"Failed to generate content for: {topic}")
    
    print(f"\nBatch generation completed!")
    print(f"Successful: {successful_posts} posts")
    print(f"Failed: {failed_posts} posts")
    print(f"All posts saved in: {generator.blog_dir}")

if __name__ == "__main__":
    generate_multiple_blogs()
