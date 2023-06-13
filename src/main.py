import os
import PyPDF2
import pypdfium2 as pdfium
import argparse

from tqdm.auto import tqdm
from utils import *


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", dest="path", type=str, required=True)

    # Check if the file exist and if it has a supported type (img or pdf)
    path = parser.parse_args().path
    file_type = check_type(path)    
    print(f"Entered file type is : {file_type}")

    # Incase of Image
    if file_type == "img":
        
        # load and preprocess image
        img = image_preprocessing(path)
        text = parsing_text(img)
        
        # save to text file
        save_path = f"{path[:-4]}.txt"
        print(f"Saved to :{save_path}")
        with open(save_path, 'w') as file:
            file.writelines("\n".join(text))

    # Incase of pdf
    elif file_type == "pdf":
        
        reader = PyPDF2.PdfReader(path)
        number_of_pages = len(reader.pages)

        os.mkdir(f"{path[:-4]}")
        for i in tqdm(range(number_of_pages)):
            page = reader.pages[i]
            text = page.extract_text()
    
            save_path = f"{path[:-4]}/{i}.txt"
            print(f"Page {i} Saved to :{save_path}")

            if text:
                text = text.replace("\n", "")
                text = create_lines(text)
                with open(save_path, 'w') as file:
                    file.writelines("\n".join(text))

            else:
                
                pdf = pdfium.PdfDocument(path)
                page = pdf[i]
                image = page.render(scale=2).to_pil()
                image.save("tmp.jpg")

                img = image_preprocessing("tmp.jpg")
                text = parsing_text(img)
                
                with open(save_path, 'w') as file:
                    file.writelines("\n".join(text))

                os.remove("tmp.jpg")