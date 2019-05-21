import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))    
file_processed = []
for (dirpath, dirnames, filenames) in os.walk(os.path.join(APP_ROOT, 'processed_images/')):
    file_processed.extend(filenames)

file_source = []
for (dirpath, dirnames, filenames) in os.walk(os.path.join(APP_ROOT, 'Images/')):
    file_source.extend(filenames)

processed_image_path = os.path.join(APP_ROOT, 'processed_images/', file_processed[0])    
(len(file_processed[0]) - len(file_source[0]))
method = file_processed[0][:(len(file_processed[0]) - len(file_source[0]))]
print(method)
print(file_processed, file_source)