#This file creates minimal json for 2nd level randomise output reports 
#generated by feat.
#
# =============================================================================
#
# Fields that could not be filled:
#
# - ErrorModel_hasErrorDependence
# - ErrorModel_dependenceMapWiseDependence
# - ResidualMeanSquaresMap_atLocation (Although we have coded for the case that
#   the _glm_sigma_sqr map has been saved in the stats directory)
#
# =============================================================================
#

import os
import glob
import nibabel as nib
import json
import numpy as np

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
    
def getErrorModel_hasErrorDistribution(randomisedir):
    
    #Always normal
    return('obo_NormalDistribution')
    
def getGrandMeanMap_atLocation(randomisedir):
    
    return(os.path.join(
            randomisedir, 'mean_func.nii.gz'))
    
def getMaskMap_atLocation(randomisedir):
    
    return(os.path.join(
            randomisedir, 'mask.nii.gz'))

def getCoordinateSpace_inWorldCoordinateSystem(randomisedir):
    
    #This is only for group level and therefore we can't get more specific
    # detail on registration.
    
    n = nib.load(os.path.join(
            randomisedir, 'mean_func.nii.gz'))
    header = n.header
    
    if header['qform_code'] == 4:
        return('MNICoordinateSystem')
    elif header['qform_code'] == 3:
        return('TalairachCoordinateSystem')
    else:
        return('CustomCoordinateSystem')
        
def getErrorModel_errorVarianceHomogeneous(randomisedir):
    
    #The error model is always homogeneous for randomise.
    return(True)
    
def getErrorModel_varianceMapWiseDependence(randomisedir):
    
    #The variance is estimated per voxel.
    return('nidm_IndependentParameter')

def getModelParameterEstimation_withEstimationMethod(randomisedir):
    
    #This is always OLS
    return('obo_OrdinaryLeastSquaresEstimation')
    
def getResidualMeanSquaresMap_atLocation(randomisedir):
    
    stat_dir = os.path.join(randomisedir, 'cope1.feat', 'stats')
    
    #Find the images.
    sigma2_group_file = os.path.join(stat_dir,
                                     '_glm_sigmasqr.nii.gz')
    sigma2_sub_file = os.path.join(stat_dir,
                                   'varcope1.nii.gz')
    
    if os.path.exists(sigma2_group_file):
        # Read in each image.
        sigma2_group_img = nib.load(sigma2_group_file)
        sigma2_group = sigma2_group_img.get_data()
    
        sigma2_sub_img = nib.load(sigma2_sub_file)
        sigma2_sub = sigma2_sub_img.get_data()
        
        # Make a temporary residual mean squares map.
        residuals_file = os.path.join(stat_dir,
                                      'calculated_sigmasquareds.nii.gz')
    
        residuals_img = nib.Nifti1Image(sigma2_group + sigma2_sub,
                                        sigma2_sub_img.get_qform())
        nib.save(residuals_img, residuals_file)
        return(residuals_file)
        
    else:
        return('')
        
def getCoordinateSpace_voxelUnits(randomisedir):
    
    #Read in the header of the mean functional image.
    n = nib.load(os.path.join(
            randomisedir, 'mean_func.nii.gz'))
    header = n.header
    
    #If there are different units used for different spacial dimensions, there 
    #might be 4 reported units (x, y, z and t).
    if len(header.get_xyzt_units()) == 4:
        return([header.get_xyzt_units()[0],
                header.get_xyzt_units()[1],
                header.get_xyzt_units()[2]])
    #Otherwise there will just be two (xyz and t).
    else:
        return([header.get_xyzt_units()[0]]*3)
        
#==============================================================================
# Get contrast information.
#==============================================================================

#def getStatisticMap_contrastName(randomisedir, contrastNum):
    
def getStatisticMap_contrastName(randomisedir):
    
    #T-Stats first.
    
    desConFile = os.path.join(randomisedir, 'design.con')
    
    conNameList = []
    #Get list of contrast names
    with open(desConFile, 'r') as dcFile:
        
        for line in dcFile:
            
            if '/ContrastName' in line:
                
                conNameList.append(line.split('\t', 1)[1].replace('\n', '').strip())
                
    numOfTCons = len(conNameList)
                
    #Then F-Stats.
    desFsfFile = os.path.join(randomisedir, 'design.fsf')
    
    #Get list of contrast names
    with open(desFsfFile, 'r') as dfFile:
        
        numOfFCons = 0
        nextLine = False
        for line in dfFile:
            
            if 'fmri(nftests_real)' in line:
                
                numOfFCons = line.split(' ')[2]
                numOfFCons = int(numOfFCons.replace('\n', ''))
                break
           
        FConMat = np.array([[0]*numOfTCons]*numOfFCons)
        
        rowInd = -1
        colInd = -1
        
        for line in dfFile:
           
            if nextLine:
                
                FConMat[rowInd, colInd] = int(line.split(' ')[-1].replace('\n', ''))
                nextLine = False
                
            if 'F-test' in line and 'element' in line:
               
               splitLineArray = line.split(' ')
               rowInd = int(splitLineArray[2])-1
               colInd = int(splitLineArray[4].replace('\n', ''))-1
               nextLine = True
        
        print(FConMat)
        
        #TODO - change matrix into names
        #e.g.
        #
        # [[1 0],             ['c1',
        #  [0 1],     ---->    'c2',
        #  [1 1]]              'c1 & c2']
        
    return(conNameList)
    
def getContrastWeightMatrix_value(randomisedir):
    
    desConFile = os.path.join(randomisedir, 'design.con')

    #Get list of T contrast vectors
    with open(desConFile, 'r') as dcFile:
        
        insideMatrix = False
        
        conValList = []
        for line in dcFile:
            
            if insideMatrix:
                
                conValList.append('[' + line.replace('\n', '').strip() + ']')
            
            if '/Matrix' in line:
                
                insideMatrix = True
                
    return(conValList)
    
#def get

gfeatdir = '/home/tommaullin/Documents/temp3+++.gfeat'
#gfeatdir = '/Users/maullz/Desktop/pytreat_nidmrandomise/level2.gfeat'

print(getStatisticMap_contrastName(gfeatdir))
