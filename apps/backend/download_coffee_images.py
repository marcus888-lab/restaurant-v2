#!/usr/bin/env python3
"""
Download coffee images from Unsplash for the Coffee Shop app.
Uses Unsplash's free API to get high-quality coffee images.
"""
import os
import requests
from typing import Dict, List
import time

# Unsplash API configuration
# Using demo client ID (rate limited but works for our needs)
UNSPLASH_ACCESS_KEY = "YOUR_ACCESS_KEY"  # Optional: Add your own key for higher limits

# Coffee images to download with search queries
COFFEE_IMAGES = {
    # Espresso category
    "cappuccino.jpg": "cappuccino coffee",
    "latte.jpg": "latte coffee art",
    "mocha.jpg": "mocha coffee chocolate",
    "caramel-macchiato.jpg": "caramel macchiato coffee",
    "flat-white.jpg": "flat white coffee",
    
    # Filter coffee
    "pour-over.jpg": "pour over coffee brewing",
    "americano.jpg": "americano black coffee",
    
    # Cold brew
    "cold-brew.jpg": "cold brew coffee glass",
    "iced-latte.jpg": "iced latte coffee",
    
    # Specialty
    "matcha-latte.jpg": "matcha latte green tea",
    "taro-latte.jpg": "purple taro latte drink",
    "red-velvet-latte.jpg": "red velvet latte coffee",
}

# Direct URLs to high-quality coffee images from Unsplash (no API key needed)
DIRECT_IMAGE_URLS = {
    # Using Unsplash's direct download URLs with proper attribution
    "cappuccino.jpg": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=800&h=800&fit=crop",  # Cappuccino with foam art
    "latte.jpg": "https://images.unsplash.com/photo-1561882468-9110e03e0f78?w=800&h=800&fit=crop",  # Latte art
    "mocha.jpg": "https://images.unsplash.com/photo-1578314675249-a6910f80cc4e?w=800&h=800&fit=crop",  # Mocha with chocolate
    "caramel-macchiato.jpg": "https://images.unsplash.com/photo-1599398054066-846f28917f38?w=800&h=800&fit=crop",  # Caramel coffee
    "flat-white.jpg": "https://images.unsplash.com/photo-1577968897966-3d4325b36b61?w=800&h=800&fit=crop",  # Flat white
    
    "pour-over.jpg": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800&h=800&fit=crop",  # Pour over brewing
    "americano.jpg": "https://images.unsplash.com/photo-1521302080334-4bebac2763a6?w=800&h=800&fit=crop",  # Black coffee
    
    "cold-brew.jpg": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=800&h=800&fit=crop",  # Cold brew in glass
    "iced-latte.jpg": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=800&h=800&fit=crop",  # Iced coffee
    
    "matcha-latte.jpg": "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?w=800&h=800&fit=crop",  # Matcha latte
    "taro-latte.jpg": "https://images.unsplash.com/photo-1571328003758-4a3921661729?w=800&h=800&fit=crop",  # Purple drink
    "red-velvet-latte.jpg": "https://images.unsplash.com/photo-1594631252845-29fc4cc8cde9?w=800&h=800&fit=crop",  # Red coffee drink
}


def download_image(url: str, filename: str, output_dir: str = "static/images") -> bool:
    """Download an image from URL and save to file."""
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        
        # Skip if already exists
        if os.path.exists(filepath):
            print(f"✓ {filename} already exists, skipping...")
            return True
        
        print(f"⬇️  Downloading {filename}...")
        
        # Download image
        headers = {
            'User-Agent': 'Coffee Shop App/1.0'
        }
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        # Save to file
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Downloaded {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to download {filename}: {str(e)}")
        return False


def main():
    """Download all coffee images."""
    print("☕ Coffee Shop Image Downloader")
    print("=" * 50)
    
    success_count = 0
    total_count = len(DIRECT_IMAGE_URLS)
    
    print(f"\n📥 Downloading {total_count} coffee images...\n")
    
    for filename, url in DIRECT_IMAGE_URLS.items():
        if download_image(url, filename):
            success_count += 1
        
        # Small delay to be respectful to the server
        time.sleep(0.5)
    
    print(f"\n✨ Download complete! {success_count}/{total_count} images downloaded.")
    
    # Print attribution notice
    print("\n📸 Image Attribution:")
    print("These images are from Unsplash (https://unsplash.com)")
    print("Please credit photographers when using in production.")


if __name__ == "__main__":
    main()