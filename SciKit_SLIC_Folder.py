import SciKit_SLIC_SingleImage as SLIC
import sys
import glob

def SciKit_SLIC_Folder(input_Dir):
    file_list = glob.glob(input_Dir+'/*.png')
    i = 0
    for file in file_list:
        print ">>>>>>>>>"
        print "%d -th file: %s" %(i,file)
        SLIC.SciKit_SLIC_SingleImage(file)
        i = i+1

    print "-------------"
    print "Done"



if __name__ == '__main__':
    if len(sys.argv) == 2:
        input_Dir = sys.argv[1]
        SciKit_SLIC_Folder(input_Dir)
    else:
        print "SciKit_SLIC_Folder inputFolder"