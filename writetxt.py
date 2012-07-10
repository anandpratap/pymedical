from account.models import*


def _writefirm():
    tmp = medicinefirm.object.all()
    for i in tmp:
        cmd = "echo '"
        cmd += i.name + "' >> /home/maverick/Dropbox/projects/medical/log/medicinefirm.log"
        os.system(cmd)


def _writetype():
    tmp = medicinetype.object.all()
    for i in tmp:
        cmd = "echo '"
        cmd += i.name + "' >> /home/maverick/Dropbox/projects/medical/log/medicinetype.log"
        os.system(cmd)

def _writeshop():
    tmp = pharmashop.object.all()
    for i in tmp:
        cmd = "echo '"
        cmd += i.name + "&&&" + i.telephone + "' >> /home/maverick/Dropbox/projects/medical/log/medicineshop.log"
        os.system(cmd)


def _writemedicine():
    tmp = medicine.object.all()
    for i in tmp:
        cmd = "echo '"
        cmd += i.name + "&&&" + i.medicinetype + "&&&" + i.medicinefirm + "' >> /home/maverick/Dropbox/projects/medical/log/medicineshop.log"
        os.system(cmd)

_writefirm()
_writetype()
_writeshop()
_writemedicine()
