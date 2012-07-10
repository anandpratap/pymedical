from models import*
import os
#from pygooglechart import QRChart
def writemedicinefile():
    medicines = medicine.objects.all()
    for i in medicines:
        cmd = "echo '"
        cmd += i.name + "&&&&" + i.medicinefirm.name + "&&&&" + i.medicinetype.name + "' >> /home/maverick/Dropbox/projects/medical/log/medicinelist.log"
        os.system(cmd)

def readmedicinefile():
    a = file('/home/maverick/Dropbox/projects/medical/log/medicinelist.log')
    for i in a:
        tmp = i.replace("\n",'').split('&&&&')
        medicine_name = tmp[0]
        medicine_firm = tmp[1]
        medicine_type = tmp[2]
        is_found_f = False
        is_found_t = False
        for i in medicinefirm.objects.all():
            if medicine_firm.upper().replace(" ",'') == i.name.upper().replace(" ",''):
                is_found_f = True
                firm_obj = i
        if is_found_f == False:
            tmp_firm = medicinefirm(name=medicine_firm)
            tmp_firm.save()
            firm_obj = tmp_firm
       
        for i in medicinetype.objects.all():
            if medicine_type.upper().replace(" ",'') == i.name.upper().replace(" ",''):
                is_found_t = True
                type_obj = i
        
        if is_found_t == False:
            tmp_type = medicinetype(name=medicine_type)
            tmp_type.save()
            type_obj = tmp_type
        
        is_found = False
        for i in medicine.objects.all():
            if medicine_name.upper().replace(" ",'') == i.name.upper().replace(" ",''):
                is_found = True
        if is_found == False:
            tmp_med = medicine(name=medicine_name,medicinetype = type_obj, medicinefirm=firm_obj)
            tmp_med.save()

def extract_medicine_detail(medicine_):
    seperator = "___"
    detail = medicine_.split(seperator)
    return detail
def extract_tablets_list(string):
    seperator = "&&&"
    detail = string.split(seperator)
    return detail

def qrcode(_str, filename):
  # Create a 125x125 QR code chart
    chart = QRChart(125, 125)
  # Add the text
    chart.add_data(_str)
  # "Level H" error correction with a 0 pixel margin
    chart.set_ec('H', 0)
  # Download
    chart.download(filename)
