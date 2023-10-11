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
OUTDIR = "static/Image/"

#treatment options
treatment_options = {
        1:"Conversion",
        2:"Clean",
        3:"Transcribe",
}
#       conversion
#       transcribe

supported_image_exten =['JPG', 'PNG', 'BLP', 'BMP', 'WEBP', 'TIFF', 'TGA', 'SPIDER', 'SGI', 'PPM', 'MSP', 'JPEG', 'IM', 'ICO', 'ICNS', 'GIF', 'EPS', 'DIB', 'DDS']
supported_video_exten = ["mp4"]
supported_sound_exten = ["mp3"]

def treat_image(media_dic):
        if(media_dic.get("treatment") == "Conversion"):
                
                conversion_medium = media_dic.get("OutputExtension")
                if conversion_medium in supported_image_exten:
                        pass
                else:
                        print("failed, requested file type is not supported")
                        
                
                if media_dic.get("fileExtension") == conversion_medium:
                        conversion_medium = "PNG"
                
                try:
                        output_file = OUTDIR+media_dic.get("fileSurname")+"."+conversion_medium
                        img = Image.open(media_dic.get("filePath")) 
                        img.save(output_file)
                        return(output_file)
                except Exception as e:
                        return(f"Failed to convert the image from {media_dic.get('fileExtension')} to {conversion_medium}",e)
        elif (media_dic.get("treatment") == "Transcribe"):
                img = cv2.imread(media_dic.get("filePath"))
                
                text_in_image = pytesseract.image_to_string(img)
                pdf_image = pytesseract.image_to_pdf_or_hocr(img)
                
                make_pdf = "yes"
                if(make_pdf == "yes"):
                        with open(f'{OUTDIR}{media_dic.get("fileSurname")}.pdf', 'w+b') as f:
                                f.write(pdf_image)
                        return(f"{text_in_image} is now available in as a pdf {media_dic.get('fileSurname')}.pdf")
                

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
                        return(f"Failed to convert the image from {media_dic.get('fileExtension')} to {conversion_medium}")


def id_file(media_file,form_data):
        file_name, file_exten = media_file.split('.')
        
        file_exten = file_exten.upper()
        
        if  file_exten in supported_image_exten:
                media_type = "img"
        elif file_exten in supported_video_exten:
                media_type = "vid"
        elif file_exten in supported_sound_exten:
                media_type = "mus"
        else:
                return(f"failed to assign {media_file} to a type")
        
                        
        media_dic = {
                "type" : media_type,
                "filePath" : INPUTDIR+media_file,
                "fileSurname" : file_name,
                "fileExtension": file_exten,
                "treatment": form_data["treatment"] ,#options Conversion Clean
                "OutputExtension":  form_data["convert_to"]
        }
        return(media_dic)

def sage_start(media_file,form_data):
        
        media_dic = id_file(media_file,form_data)
        
        if (media_dic.get("type"))  == "img":
                #output_file_path = treat_image(media_dic) 
                return(treat_image(media_dic) )
        elif (media_dic.get("type"))  == "vid":
                return(treat_video(media_dic))
        elif (media_dic.get("type"))  == "mus":
                return(treat_sound(media_dic))

        #return(output_file_path)

'''if __name__ == "__main__":
        sage_start()'''