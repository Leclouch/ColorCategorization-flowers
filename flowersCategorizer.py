import os
import shutil
from PIL import Image
import numpy as np

def categorize_image(image_path, output_folder):
    # Membagi image menjadi 3 katregori warna
    try:
        img = Image.open(image_path).convert('RGB')
        w, h = img.size
        
        # cari tengah gambar dan membuat jarak terpendek ke pinggir sebagai radius
        center_x, center_y = w // 2, h // 2
        radius = int(min(w, h) * 1)
        
        # create a circle mask
        mask = Image.new('L', (w, h), 0)    # buat gambar baru grayscale seukuran image itu, warna hitam (0)
        pixels = mask.load()                # supaya bisa akses smeu apixel di gambar
        for x in range(w):
            for y in range(h):
                if (x - center_x)**2 + (y - center_y)**2 <= radius**2: #untuk pixel yang lokasinya masih didalam lingkaran kita warnai putih (255)
                    pixels[x, y] = 255
        
        # Apply mask to image
        img.putalpha(mask)          # pixel diluar lingkaran menjadi transparan
        img_array = np.array(img)   # mengubah img menjadi array numpy
        
        # Get non-transparent pixels
        alpha = img_array[:, :, 3]                      # mengambil semua value alpha dari gambar sebagai 2d grid
        flower_pixels = img_array[alpha > 0][:, :3]     # untuk yang alpha nya > 0, ambil grid value RGB (value alhpa didrop) 
        
        if len(flower_pixels) == 0:     # kalau gada pixel disini kembalikan "none"
            return None
        
        # Get dominant color
        r_mean = flower_pixels[:, 0].mean()     # ambil rata2 value RED dari semua pixel
        g_mean = flower_pixels[:, 1].mean()     # ambil rata2 value GREEN dari semua pixel
        b_mean = flower_pixels[:, 2].mean()     # ambil rata2 value BLUE dari semua pixel
        
        dominant = np.argmax([r_mean, g_mean, b_mean]) # cari value terbesar dan return indexnya (misal r_mean paling besar maka return 0)
        colors = ['red', 'green', 'blue']              # buat list strings warna sesuai urutan rgb 
        return colors[dominant]                        # return string warna (misal dominant = 0 maka colors[0] = 'red')
    
    except Exception as e:      # jika ada error maka errornya akan tersampaikan dan tidak ngecrash
        print(f"Error: {e}")
        return None

def main():
    source = input("Source folder: ")   # ambil sumber folder dataset
    output = input("Output folder: ")   # ambil tujuan folder
    
    if not os.path.exists(source):          # jika folder sumber tidak ada
        print("Source folder not found!")   # kasih tau kalau gak ada
        return                              # stop code
    
    # Create output folders
    for color in ['red', 'green', 'blue']:                          # loop tiap iterasi value 
        os.makedirs(os.path.join(output, color), exist_ok=True)     # membuat folder baru bernama value color sekarang di folder "output" 
                                                                    # exist_ok supaya jika sudah ada folder red green blue didalamnya code tidak complain
    
    # Process images
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}   # extension yang dibolehkan
    count = 0  
    
    for filename in os.listdir(source):             # loop smeua file di sumber
        file_path = os.path.join(source, filename)  # membuat path untuk tiap file image dengan menggabungkan path sumber dengan file
        
        if not os.path.isfile(file_path):   # jika bukan suatu file (melainkan folder) skip iterasi ini
            continue
        
        if os.path.splitext(filename)[1].lower() not in image_extensions:   # jika extension pada nama file tidak ada di list extension maka skip iterasi ini
            continue
        
        color = categorize_image(file_path, output) # mendapatkan value color dari fungsi
        
        if color:                                           # jika value nya wanra (bukan none)
            dest = os.path.join(output, color, filename)    # membuat destinasi "folder_sumber" / "color" / "nama_file"
            shutil.move(file_path, dest)                    # memindahkan file tersebur dari "filepath"(lokasi file sekarang) ke destinasi yang telah dibuat
            print(f"{filename} → {color}")                  # Menulis di terminal hasil sortiran file terebut ditaro dimana
            count += 1                                      # menghitung jumlah file yang telah di sort
    
    print(f"\nDone! {count} images categorized.")           # di taro di terminal

if __name__ == "__main__":
    main()