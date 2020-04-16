#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os, io
from google.cloud import vision
from google.cloud.vision import types
import pandas as pd
import re
from iteration_utilities import unique_everseen


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'google vision api Json path '



client = vision.ImageAnnotatorClient()


image_path = r'Image path'



try:

    # read image file in rgb format 
    with io.open (image_path, 'rb') as image_file:
        content = image_file.read()
        
    # extract text from image and return response     
    image = vision.types.Image(content = content)
    response = client.document_text_detection(image=image)
    docText = response.full_text_annotation.text
except:
    print('error: check file or api is correct')

# split the data based on line by line 
docText_list = docText.splitlines( )

try:
    Asianet_bill_details = [] 

    for i in range(len(docText_list)):

        data = docText_list[i]
        data = data.strip()
        #print(data)

        # extracting required information from data

        if 'Name' in data :  

            try:            
                Name = data.split('Name:')[-1]

                Asianet_bill_details.append({'Consumer Name':Name})

            except:
                Name = ""
                Asianet_bill_details.append({'Consumer Name':Name})

        if 'Sub Code' in data :  

            try:            
                Id = data.split('Sub Code')[-1]

                Asianet_bill_details.append({'Consumer Id':Id})

            except:
                Id = ""
                Asianet_bill_details.append({'Consumer Id':Id})

        if 'MOBILE' in data :

            PHONE = re.findall( r'[697]\d{1,2}.\d{2,3}.\d{2,3}.\d{0,2}',data)

            try:

                PHONE = PHONE[0].strip()

            except:

                PHONE = ''
                Asianet_bill_details.append({'Mobile Number':PHONE})

            if not PHONE:

                PHONE = ''
                Asianet_bill_details.append({'Mobile Number':PHONE})

            else:

                Asianet_bill_details.append({'Mobile Number':PHONE})

        if 'EMAIL' in data:

            Email = re.findall('\S+@\S+', data)

            if not Email:

                Email = ''
                Asianet_bill_details.append({'Email Id':Email})

            else:

                Asianet_bill_details.append({'Email Id':Email[0]})

        if 'Due Date' in data :
            try:

                date = data.split('Due Date: ')[-1]
                Asianet_bill_details.append({'Due Date':date})

            except:

                pass
        else:
            #date = ''
            #Asianet_bill_details.append({'Due Date':date})
            pass
        if 'Total Amount Due' in data :

            j = i+1
            Amount = docText_list[j]
            Asianet_bill_details.append({'Amount to pay': Amount})

        else:

            pass

except:
    print('error')




# unique_everseen to find the unique values 
details_unique= list(unique_everseen(Asianet_bill_details))    
            
print(details_unique)






