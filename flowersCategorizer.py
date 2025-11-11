import os
import shutil
from PIL import Image
import numpy as np

def categorize_image(image_path, output_folder):
    """Membagi """
    try:
        img = Image.open(image_path).convert('RGB')
        w, h = img.size
        
        # Extract center circle (45% of image size)
        center_x, center_y = w // 2, h // 2
        radius = int(min(w, h) * 0.45)
        
        # Create mask for circle
        mask = Image.new('L', (w, h), 0)
        pixels = mask.load()
        for x in range(w):
            for y in range(h):
                if (x - center_x)**2 + (y - center_y)**2 <= radius**2:
                    pixels[x, y] = 255
        
        # Apply mask to image
        img.putalpha(mask)
        img_array = np.array(img)
        
        # Get non-transparent pixels
        alpha = img_array[:, :, 3]
        flower_pixels = img_array[alpha > 0][:, :3]
        
        if len(flower_pixels) == 0:
            return None
        
        # Get dominant color
        r_mean = flower_pixels[:, 0].mean()
        g_mean = flower_pixels[:, 1].mean()
        b_mean = flower_pixels[:, 2].mean()
        
        dominant = np.argmax([r_mean, g_mean, b_mean])
        colors = ['red', 'green', 'blue']
        return colors[dominant]
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    source = input("Source folder: ")
    output = input("Output folder: ")
    
    if not os.path.exists(source):
        print("Source folder not found!")
        return
    
    # Create output folders
    for color in ['red', 'green', 'blue']:
        os.makedirs(os.path.join(output, color), exist_ok=True)
    
    # Process images
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    count = 0
    
    for filename in os.listdir(source):
        file_path = os.path.join(source, filename)
        
        if not os.path.isfile(file_path):
            continue
        
        if os.path.splitext(filename)[1].lower() not in image_extensions:
            continue
        
        color = categorize_image(file_path, output)
        
        if color:
            dest = os.path.join(output, color, filename)
            shutil.move(file_path, dest)
            print(f"✓ {filename} → {color}")
            count += 1
    
    print(f"\nDone! {count} images categorized.")

if __name__ == "__main__":
    main()