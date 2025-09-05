#!/usr/bin/env python3
"""
Script to add AOS (Animate On Scroll) animations to all HTML pages
"""

import os
import re
from pathlib import Path

def add_aos_to_page(file_path):
    """Add AOS library and animations to a single HTML page"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if AOS is already included
    if 'aos.css' in content and 'aos.js' in content:
        print(f"AOS already present in {file_path}")
        return
    
    # Add AOS CSS
    if 'aos.css' not in content:
        css_pattern = r'(<link href="https://cdn\.jsdelivr\.net/npm/bootstrap@5\.3\.3/dist/css/bootstrap\.min\.css" rel="stylesheet">)'
        css_replacement = r'\1\n    <link rel="stylesheet" href="https://unpkg.com/aos@2.3.0/dist/aos.css">'
        content = re.sub(css_pattern, css_replacement, content)
    
    # Add AOS JS and initialization
    if 'aos.js' not in content:
        # Find the last script tag before </body>
        script_pattern = r'(</body>)'
        script_replacement = r'''    <script src="https://unpkg.com/aos@2.3.0/dist/aos.js"></script>
    <script>
        AOS.init({
            duration: 1200,
        })
    </script>

\1'''
        content = re.sub(script_pattern, script_replacement, content)
    
    # Add basic animations to common elements
    animations_added = 0
    
    # Banner headings
    banner_pattern = r'(<h2[^>]*class="[^"]*banner-main[^"]*"[^>]*>)([^<]+)(</h2>)'
    if not re.search(r'data-aos=', content):
        content = re.sub(banner_pattern, r'\1<span data-aos="fade-up">\2</span>\3', content)
        animations_added += 1
    
    # After banner content
    after_banner_pattern = r'(<div class="after-banner-main"[^>]*>)'
    if not re.search(r'data-aos=', content):
        content = re.sub(after_banner_pattern, r'\1 data-aos="fade-up"', content)
        animations_added += 1
    
    # Section headings
    heading_pattern = r'(<h2[^>]*class="[^"]*theme[^"]*"[^>]*>)([^<]+)(</h2>)'
    if not re.search(r'data-aos="fade-up"', content):
        content = re.sub(heading_pattern, r'\1<span data-aos="fade-up">\2</span>\3', content)
        animations_added += 1
    
    # Destination cards
    card_pattern = r'(<div class="col-[^"]*"[^>]*>)(<div class="destination-card)'
    if not re.search(r'data-aos="zoom-in"', content):
        content = re.sub(card_pattern, r'\1 data-aos="zoom-in" data-aos-delay="100"\2', content)
        animations_added += 1
    
    # Blog cards
    blog_card_pattern = r'(<div class="col-[^"]*"[^>]*>)(<div class="card blog-card)'
    if not re.search(r'data-aos="fade-up"', content):
        content = re.sub(blog_card_pattern, r'\1 data-aos="fade-up" data-aos-delay="100"\2', content)
        animations_added += 1
    
    # Write the updated content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {file_path} - Added {animations_added} animations")

def main():
    """Main function to process all HTML files"""
    
    # Get all HTML files in the current directory
    html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'add_aos_animations.py']
    
    print(f"Found {len(html_files)} HTML files to process")
    
    for html_file in html_files:
        try:
            add_aos_to_page(html_file)
        except Exception as e:
            print(f"Error processing {html_file}: {e}")
    
    print("AOS animations added to all pages!")

if __name__ == "__main__":
    main()
