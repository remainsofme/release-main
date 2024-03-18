import sqlite3
import os
import pypdf
from PIL import Image, ImageDraw, ImageFont,ImageOps
import math
import json

def allowed_file(filename):
   allowed_extension=['jpeg',"png",'jpg']
   return '.' in filename and filename.rsplit('.',1)[1].lower() in allowed_extension


def resize_pictures():
   pillow_object_list=[]
   image_dir='static/image'
   pictures=os.listdir(image_dir)
   for picture in pictures:
      url='static/image/'+picture
      pillow_object=Image.open(url)
      if pillow_object.width<=1240 and pillow_object.height<=1550:
        new=pillow_object.resize((pillow_object.width*8,pillow_object.height*8))
        new.thumbnail((1240,1550))
        pillow_object_list.append(new)
      else:
         pillow_object.thumbnail((1240,1550))
         pillow_object_list.append(pillow_object)
   return pillow_object_list
   print(pillow_object_list)
   
def table():
    if 'pdfs' not in os.listdir('static'):
      os.mkdir('static/pdfs')
    if 'image' not in os.listdir('static'):
      os.mkdir('static/image')
    image_dir='static/image'
    pictures=os.listdir(image_dir)
    picture_table=[]
    index=0
    for picture in pictures:
        picture_record=(index, picture, "")
        picture_table.append(picture_record)
        index=index+1
    print(picture_table)
    return picture_table


def parse_pdf(table_object):
   if 'image' not in os.listdir('static'):
      os.mkdir('static/image')
   if 'pdfs' not in os.listdir('static'):
      os.mkdir('static/pdfs')
   if 'result.pdf' in os.listdir('static/pdfs'):
      print('heelelel')
      os.remove('static/pdfs/result.pdf')
   else:
      pass
   pad=200
   pad_y=200
   my_font=ImageFont.truetype('static/font/ipam.ttc', 30)
   # the index of the last record
   last_index=table_object[-1][0]
   # number of pages when grouped into 4
   page_number=math.ceil((last_index+1)/4)
   # the number of pictures in the last page
   photo_number_last_page=(last_index+1)%4
   

   pillow_object_list=[]
   image_dir='static/image/'
   for element in range(len(table_object)):
      pillow_object=Image.open(image_dir+table_object[element][1])
      if pillow_object.width<=(1240-pad*2) and pillow_object.height<=1550-pad_y*2:
        new=pillow_object.resize((pillow_object.width*8,pillow_object.height*8))
        new.thumbnail((1240-pad*2,1550-pad_y*2))
        pillow_object_list.append(ImageOps.exif_transpose(new))
      else:
         pillow_object.thumbnail((1240-pad*2,1550-pad_y*2))
         pillow_object_list.append(ImageOps.exif_transpose(pillow_object))
   print(pillow_object_list)
   annotation_list=[]
   for record in table_object:
       # fill p_o_list with picture
       annotation_list.append(record[2])

   multiplier=1
   size=(2480*multiplier,3508*multiplier)
  
   page_list=[]
   for page_number in range(page_number-1):
      page=Image.new(mode='RGB',size=size,color='white')
      page_text=ImageDraw.Draw(page)
      pictures_one_page=pillow_object_list[4*page_number:4*page_number+4]
      annotation_list_one_page=annotation_list[4*page_number:4*page_number+4]
      page.paste(pictures_one_page[0],(pad,pad_y))
      page_text.text((pad,pictures_one_page[0].height+60+pad_y),annotation_list_one_page[0],fill=(0,0,0),font=my_font)
      page.paste(pictures_one_page[1],(1240*multiplier+pad,pad_y))
      page_text.text((1240+pad,pictures_one_page[1].height+60+pad_y),annotation_list_one_page[1],fill=(0,0,0),font=my_font)
      page.paste(pictures_one_page[2],(pad,1750*multiplier+pad_y))
      page_text.text((pad,pictures_one_page[2].height+60+1750+pad_y),annotation_list_one_page[2],fill=(0,0,0),font=my_font)
      page.paste(pictures_one_page[3],(1240*multiplier+pad,1750*multiplier+pad_y))
      page_text.text((1240+pad,pictures_one_page[3].height+60+1750+pad_y),annotation_list_one_page[3],fill=(0,0,0),font=my_font)
      page_list.append(page)
   print(-photo_number_last_page)
   print(pillow_object_list)
   pictures_last_page=pillow_object_list[-photo_number_last_page:]
   annotation_last_page=annotation_list[-photo_number_last_page:]
   last_page=Image.new(mode='RGB',size=size,color='white')
   last_page_text=ImageDraw.Draw(last_page)
   try:
      last_page.paste(pictures_last_page[0],(pad,pad_y))
      last_page_text.text((pad,pictures_last_page[0].height+60+pad_y),annotation_last_page[0],fill=(0,0,0),font=my_font)
      last_page.paste(pictures_last_page[1],(1240*multiplier+pad,pad_y))
      last_page_text.text((1240+pad,pictures_last_page[1].height+60+pad_y),annotation_last_page[1],fill=(0,0,0),font=my_font)
      last_page.paste(pictures_last_page[2],(pad,1750*multiplier+pad_y))
      last_page_text.text((pad,pictures_last_page[2].height+60+1750+pad_y),annotation_last_page[2],fill=(0,0,0),font=my_font)
      last_page.paste(pictures_last_page[3],(1240*multiplier+pad,1750*multiplier+pad_y))
      last_page_text.text((1240+pad,pictures_last_page[3].height+60+1750+pad_y),annotation_last_page[3],fill=(0,0,0),font=my_font)
   except Exception:
      print(Exception)
   page_list.append(last_page)


   merger=pypdf.PdfMerger()
   n=0
   tem_file_list=[]
   for page in page_list:
      tem_file_list.append(str(n)+'.pdf')
      page.save(str(n)+'.pdf')
      merger.append(str(n)+'.pdf')
      n=n+1
   merger.write('static/pdfs/result.pdf')
   merger.close()
   for tem_file in tem_file_list:
      os.remove(tem_file)
   for file in os.listdir('static/image'):
      os.remove('static/image'+'/'+file)

   


   
   

       


          
   


       
       
    
    



       

    



if __name__=='__main__':
    parse_pdf(table())