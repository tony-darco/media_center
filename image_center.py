import os
import json
import logging

#image libs
import pytesseract
import cv2
from PIL import Image

#audio libs
from pydub import AudioSegment
import speech_recognition as sr

#Notes
#files names has to be full path and has to be cut short to just the name and extension

config_file = open("support.json")

INPUT_DIR = "staging/"
OUTPUT_DIR = "static/Image/"

speech_file_types = ["WAV", "AIFF", "AIFF-C", "FLAC"]

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
supported_sound_exten = ["MP3","WAV"]
def convert_image(media_dic):
    """
    Converts images from on file to another

    Args:
        media_dic (dictionary): holds necessary the file information, from file name to file extension as keys
    """
    if(media_dic["treatment"] == "convert_image"):
        out_exten = media_dic["OutputExtension"]
        if out_exten not in supported_image_exten:
            logging.error("failed, requested file type is not supported")

        #might take this out in future versions, not necessary if using the webpage??
        #changes the conversion medium cuz its the same as the image file
        if media_dic["fileExtension"] == out_exten:
            out_exten = "PNG"
            logging.info(f"Conversion medium: {out_exten}")

        try:
            #creating the new file names
            output_file = OUTPUT_DIR+media_dic["fileSurname"]+"."+out_exten
            img = Image.open(media_dic["filePath"]) 
            img.save(output_file)
            
            logging.info(f"Converted image {media_dic['fileSurname']} from {media_dic['fileExtension']} to {out_exten}")
            logging.info(f"File saved as {output_file}")
            
            return(output_file)
        except Exception as e:
            logging.error(f"Failed to convert the image from {media_dic.get('fileExtension')} to {out_exten}",exc_info=True)
    else:
        logging.error("conversion called by error")

def treat_video(media_dic):
        print(media_dic)
        print("this file is a video file")

def text_recognition_image(media_dic):
    if (media_dic.get("treatment") == "transcribe"):
        img = cv2.imread(media_dic["filePath"])

        try:
            text_in_image = pytesseract.image_to_string(img)
        except Exception as e:
            logging.error(f"Failed to read the image {media_dic['fileSurname']}",exc_info=True)
        
        make_pdf = "no"
        if(make_pdf == "yes"):
            try:
                pdf_image = pytesseract.image_to_pdf_or_hocr(img)
                
                with open(f'{OUTPUT_DIR}{media_dic["fileSurname"]}.pdf', 'w+b') as f:
                    f.write(pdf_image)

                logging.info(f"{text_in_image} is now available in as a pdf {media_dic.get('fileSurname')}.pdf")
            except Exception as e:
                logging.error(f"Failed to pdf image file {media_dic['fileSurname']}",exc_info=True)

def convert_sound(media_dic):
    if(media_dic["treatment"] == "convert_audio"):
        out_exten = media_dic["OutputExtension"]
        if out_exten not in supported_image_exten:
            logging.error("failed, requested file type is not supported")
            return("failed")
    
        try:
            AudioSegment.from_file(media_dic["filePath"]).export(OUTPUT_DIR, format=out_exten)
        except:
            logging.error(f"Failed to convert the image from {media_dic['fileExtension']} to {out_exten}")

def text_recongiztion_audio(media_dic):
    if (media_dic["treatment"] == "transcribe"):
        input_exten = media_dic["fileExtension"]

        if input_exten not in supported_sound_exten:
            logging.error(f"{input_exten} is supported: {input_exten in supported_sound_exten}")
            return()

        try:
            if input_exten not in speech_file_types:
                AudioSegment.from_file(media_dic["filePath"]).export(format=speech_file_types[0])
        except Exception as e:
            logging.error(f"Failed to convert file to a {speech_file_types[0]}")

        try:
            sp_recon = sr.Recognizer()
            sp_recon.adjust_for_ambient_noise(media_dic["filePath"])
            audio = sp_recon.record(media_dic["filePath"])
            try:
                tn_output = sp_recon.recognize_tensorflow(audio)
                google_output = sp_recon.recognize_google_cloud(audio)


                if tn_output != google_output:
                    logging.info("the two outputs were different.")

                print(google_output)
            except:
                logging.error(f"failed to export text file")
        except Exception as e:
            logging.error(f"failed to read audio file")


def id_file(media_file, service_type, out_extension, type_transcribe):
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
        "filePath" : INPUT_DIR+media_file,
        "fileSurname" : file_name,
        "fileExtension": file_exten,
        "treatment": service_type ,#options Conversion Clean
        "OutputExtension":  out_extension,
        "type_transcribe" : type_transcribe
    }
    return(media_dic)

def image_start(media_file,form_data):
    service_type = form_data["service_select"]
    out_extension = form_data["convert_select"]
    type_transcribe = form_data["transcribe_select"]

    media_dic = id_file(media_file,service_type,out_extension,type_transcribe)
    print(service_type,media_dic["type"])
    if (media_dic["type"])  == "img" and (service_type == "convert_image"):
        #output_file_path = treat_image(media_dic) 
        return(convert_image(media_dic) )
    elif (media_dic["type"])  == "img" and (service_type == "transcribe"):
        return(text_recognition_image(media_dic))

    elif (media_dic.get("type"))  == "vid" and (service_type == "convert_video"):
        return(convert_video(media_dic))

    elif (media_dic.get("type"))  == "mus" and (service_type == "convert_audio"):
        return(convert_sound(media_dic))
    elif (media_dic.get("type"))  == "mus" and (service_type == "transcribe"):
        return(text_recongiztion_audio(media_dic))
    else:
        logging.error("couldn't find type")
        return("failed")

'''if __name__ == "__main__":
        sage_start()'''