import os
import glob
import nibabel as nib
import json

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

def getData_grandMeanScaling(randomisedir):

    #We always grand mean scale.
    return(True)

def getData_targetIntensity(randomisedir):

    #Always 10000.0
    return(10000.0)

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

def getDesignMatrix_regressorNames(randomisedir):
    regressorNames = []
    #Read in design.fsf file
    design_fsl_file = os.path.join(randomisedir,
                                   'design.fsf')

    with open(design_fsl_file, 'r') as input_file:
        lines = input_file.readlines()

    for line in lines:
        if "evtitle" in line:
            split_line = line.split('"')
            regressorNames.append(split_line[1])

    return(regressorNames)

def getParameterEstimateMaps(randomisedir):
    if os.path.isdir(os.path.join(randomisedir, 'cope1.feat')) is True: 
        pe_dir = os.path.join(randomisedir, 'cope1.feat', 'stats')
        pe_maps = glob.glob(os.path.join(pe_dir,'pe*.nii.gz'))
    else:
        pe_maps = []

    return(pe_maps)



#gfeatdir = '/home/tommaullin/Documents.gfeat'
gfeatdir = '/Users/maullz/Desktop/pytreat_nidmrandomise/level2+.gfeat'

#print(getNeuroImagingAnalysisSoftwareType(gfeatdir))
#print(getNeuroimagingAnalysisSoftware_softwareVersion(gfeatdir))
#print(getData_grandMeanScaling(gfeatdir))
#print(getData_targetIntensity(gfeatdir))
#print(getDesignMatrix_atLocation(gfeatdir))
#print(getDesignMatrix_regressorNames(gfeatdir))
#print(getParameterEstimateMaps(gfeatdir))
