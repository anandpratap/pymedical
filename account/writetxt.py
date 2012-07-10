from models import*


def _writefirm():
    tmp = medicinefirm.objects.all()
    for i in tmp:
        cmd = "echo '"
        cmd += i.name + "' >> /home/maverick/Dropbox/projects/medical/log/medicinefirm.log"
        os.system(cmd)


def _writetype():
    tmp = medicinetype.objects.all()
    for i in tmp:
        cmd = "echo '"
        cmd += i.name + "' >> /home/maverick/Dropbox/projects/medical/log/medicinetype.log"
        os.system(cmd)

def _writeshop():
    tmp = pharmashop.objects.all()
    for i in tmp:
        cmd = "echo '"
        cmd += i.name + "&&&" + i.telephone + "' >> /home/maverick/Dropbox/projects/medical/log/medicineshop.log"
        os.system(cmd)


def _writemedicine():
    tmp = medicine.objects.all()
    for i in tmp:
        cmd = "echo '"
        cmd += i.name + "&&&" + i.medicinetype.name + "&&&" + i.medicinefirm.name + "' >> /home/maverick/Dropbox/projects/medical/log/medicine.log"
        os.system(cmd)

_writefirm()
_writetype()
_writeshop()
_writemedicine()
