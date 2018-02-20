import os

def getNeuroImagingAnalysisSoftwareType(randomisedir):
    return('scr_FSL')

def getNeuroimagingAnalysisSoftware_softwareVersion(randomisedir):

    #Read in report.
    copefile = open(os.path.join(randomisedir,
                                 'cope1.feat',
                                 'report_stats.html'), 'r')
    versionNumber = -1
    
    for line in copefile:
        
        if 'Version ' in line:

            textAfterVersion = line.split('Version ')[1]
            versionNumber = textAfterVersion.split(',')[0]

    return(versionNumber)

def getDesignMatrix_atLocation(randomisedir):
    output_filename = './DesignMatrix.csv'
    #Read in design.mat file
    design_mat_file = os.path.join(randomisedir,
                                   'design.mat')

    with open(design_mat_file, 'r') as input_file:
        lines = input_file.readlines()
        
    
    with open(output_filename, 'w') as output_file:
        always_print = False
        for line in lines:
            if always_print == True:
                output_file.writelines(line)
            if "Matrix" in line:
                always_print = True
                
    return(output_filename)

gfeatdir = '/Users/maullz/Desktop/pytreat_nidmrandomise/level2.gfeat'
print(getNeuroImagingAnalysisSoftwareType(gfeatdir))
print(getNeuroimagingAnalysisSoftware_softwareVersion(gfeatdir))
print(getDesignMatrix_atLocation(gfeatdir))
