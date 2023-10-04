from PIL import Image
from pydub import AudioSegment
import os
import json
import cv2
import pytesseract

#Notes
#files names has to be full path and has to be cut short to just the name and extension

config_file = open("supportedFiles.json")
config_data = json.load(config_file)

INPUTDIR = "staging/"
OUTDIR = "backstage/"

#treatment options
treatment_options = {
        1:"Conversion",
        2:"Transcribe",
        3:"both"
}
#       conversion
#       transcribe

supported_image_exten = ["jpg","png"]
supported_video_exten = ["mp4"]
supported_sound_exten = ["mp3"]

def treat_image(media_dic):
        print(media_dic)
        print("this file is a image file")
        
        if(media_dic.get("treatment") == "conversion"):
                conversion_medium = "jpg"
                if media_dic.get("fileExtension") == conversion_medium:
                        conversion_medium = "png"
                
                try:
                        with Image.open(media_dic.get("filePath")) as img:
                                img.save(OUTDIR+media_dic.get("fileSurname")+"."+conversion_medium)
                except:
                        print(f"Failed to convert the image from {media_dic.get('fileExtension')} to {conversion_medium}")
        elif (media_dic.get("treatment") == "Transcribe"):
                img = cv2.imread(media_dic.get("filePath"))
                
                text_in_image = pytesseract.image_to_string(img)
                pdf_image = pytesseract.image_to_pdf_or_hocr(img)
                
                with open(f'{media_dic.get("fileSurname")}.pdf', 'w+b') as f:
                        f.write(pdf_image)
                        
                print(f"{text_in_image} is now available in as a pdf {media_dic.get('fileSurname')}.pdf")
                

def treat_video(media_dic):
        print(media_dic)
        print("this file is a video file")

def treat_sound(media_dic):
        print(media_dic)
        print("this file is a sound file")
        
        if(media_dic.get("treatment") == "conversion"):
                conversion_medium = "mp3"
                if media_dic.get("fileExtension") == conversion_medium:
                        conversion_medium = "wav"
                
                try:
                        AudioSegment.from_file(media_dic.get("filePath")).export(OUTDIR, format=conversion_medium)
                except:
                        print(f"Failed to convert the image from {media_dic.get('fileExtension')} to {conversion_medium}")


def id_file(media_file,treatment):
        file_name, file_exten = media_file.split('.')
        
        if  file_exten in supported_image_exten:
                media_type = "img"
        elif file_exten in supported_video_exten:
                media_type = "vid"
        elif file_exten in supported_sound_exten:
                media_type = "mus"
        else:
                return("failed")
        
                        
        media_dic = {
                "type" : media_type,
                "filePath" : "staging/"+media_file,
                "fileSurname" : file_name,
                "fileExtension": file_exten,
                "treatment": treatment
        }
        
        return(media_dic)

def main():
        #identify the file
        #use a list of supported files
        file_instage = os.listdir(INPUTDIR)
        
        list_media_files = []
        
        #Ask the type of work that sage is meant to do
        #transcribe the sound into text or print the text in the image
        media_file = input("which file would you like to work on? ")
        
        treatment = input("What would you like to do with the file:\n1.Convert\n2.Transcribe\nChoose a number 1 or 2, 3(for both): ")
        
        
        for media_file in file_instage:
                list_media_files.append(id_file(media_file,treatment_options.get(treatment)))
                
                
        for i in range(len(list_media_files)):
                
                if (list_media_files[i].get("type"))  == "img":
                        treat_image(list_media_files[i])
                        
                elif (list_media_files[i].get("type"))  == "vid":
                        treat_video(list_media_files[i])
                        
                elif (list_media_files[i].get("type"))  == "mus":
                        treat_sound(list_media_files[i])
                        
                
        return

if __name__ == "__main__":
        main()