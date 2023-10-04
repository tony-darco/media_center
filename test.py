supported_image_exten = ["jpg","png","blp","bmp","webp","tiff","tga","spider","sgi","ppm","msp","jpeg","im","ico","icns","gif","eps","dib","dds"]

new = []
for i in supported_image_exten:
    new.append(i.upper())
    
print(new)