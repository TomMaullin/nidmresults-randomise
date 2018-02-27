#This file creates minimal json for 2nd level randomise output reports 
#generated by feat.
#
# =============================================================================
#
# Fields that could not be filled as they do not exist for randomise:
#
# - ErrorModel_hasErrorDependence
# - ErrorModel_dependenceMapWiseDependence
# - ResidualMeanSquaresMap_atLocation (Although we have coded for the case that
#   the _glm_sigma_sqr map has been saved in the stats directory)
# - PeakDefinitionCriteria_maxNumberOfPeaksPerCluster
#
# =============================================================================
#
# Authors: Tom Maullin, Alex Bowring
#
# =============================================================================

import os
import glob
import nibabel as nib
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

        for i in range(len(FConMat)):
            FConName = ""
            for j in range(len(FConMat[i])):
                if FConMat[i][j] == 1:
                    FConName += 'C' + str(j+1) + ' & '
            FConName = FConName[:-3]
            conNameList.append(FConName)

    return(conNameList)
    
def getContrastWeightMatrix_value(randomisedir):
    
    desConFile = os.path.join(randomisedir, 'design.con')

    #Get list of T contrast vectors
    with open(desConFile, 'r') as dcFile:
        
        insideMatrix = False
        
        TconValList = []
        for line in dcFile:
            
            if insideMatrix:
                
                formattedLine = line.replace('\n', '').strip().split(' ')
                numericalEntries = [
                    float(formattedLine[i]) for i in range(len(formattedLine))]
                TconValList.append(numericalEntries)
            
            if '/Matrix' in line:
                
                insideMatrix = True
    
    # Now F contrast vectors.
    numOfTCons = len(TconValList)
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
    
    FconValList = []
    # Convert the Fcon matrix into the F contrasts.
    for i in range(numOfFCons):
        
        currentFCon = []
        for j in range(numOfTCons):
            if FConMat[i, j]==1:
                currentFCon.append(TconValList[j])
                
        FconValList.append(currentFCon)
        
    conValList = TconValList + FconValList
    
    return(conValList)

def getStatisticMap_statisticType(randomisedir):
    stat_dir = os.path.join(randomisedir, 'cope1.feat', 'stats')
    tstats = sorted(glob.glob(os.path.join(stat_dir, 'tstat*')))
    tstats = ["obo_TStatistic"]*len(tstats)
    fstats  = sorted(glob.glob(os.path.join(stat_dir,'fstat*')))
    fstats   = ["obo_FStatistic"]*len(fstats)
    statisticTypeList = tstats + fstats

    return(statisticTypeList)

def getStatisticMap_atLocation(randomisedir):
    stat_dir = os.path.join(randomisedir, 'cope1.feat', 'stats')
    tstats = sorted(glob.glob(os.path.join(stat_dir, 'tstat*')))
    fstats  = sorted(glob.glob(os.path.join(stat_dir,'fstat*')))
    statisticMapList = tstats + fstats

    return(statisticMapList)
    
def getClusterDefinitionCriteria_hasConnectivityCriterion(randomisedir):
    
    feat4_post_log = os.path.join(randomisedir, 'cope1.feat', 'logs', 'feat4_post')
    
    with open(feat4_post_log) as f4pl:
        
        for line in f4pl:
            
            if 'connectivity' in line:
                
                inputsInLine = line.split(' ')
                break
    
    conCrit = -1
    
    for lineElement in inputsInLine:
            
        if 'connectivity' in lineElement:
            
            conCrit = lineElement.split('=')[1]
            
    return(conCrit)
    
def getPeakDefinitionCriteria_minDistanceBetweenPeaks(randomisedir):
    
    #This option doesn't exist in FSL. 
    return(0.0)

def getContrastMap_atLocation(randomisedir):
    
    stat_dir = os.path.join(randomisedir, 'cope1.feat', 'stats')
    copes = sorted(glob.glob(os.path.join(stat_dir, 'cope*')))

    return(copes)
    
def getContrastStandardErrorMap_atLocation(randomisedir):
    
    stat_dir = os.path.join(randomisedir, 'cope1.feat', 'stats')
    copeVars = sorted(glob.glob(os.path.join(stat_dir, 'varcope*')))
    
    for i in range(len(copeVars)):
        
        # Read in the image.
        imobj = nib.load(copeVars[i], mmap=False)
        
        # display header object
        imhdr = imobj.header
        
        # extract data (as an numpy array)
        imdat = imobj.get_data().astype(float)
        
        #Record the standard errors.
        newdata = np.sqrt(imdat)
        newhdr = imhdr.copy()
        newobj = nib.nifti1.Nifti1Image(newdata, None, header=newhdr)
        nib.save(newobj, "copeSE" + str(i+1) + ".nii.gz")

    return(["copeSE" + str(i+1) + ".nii.gz" for i in range(len(copeVars))])
    
def getStatisticMap_effectDegreesOfFreedom(randomisedir):
    
    statTypes = getStatisticMap_statisticType(randomisedir)
    conVectors = getContrastWeightMatrix_value(randomisedir)
    
    erdf = ['']*len(statTypes)
    for i in range(len(conVectors)):
        
        if statTypes[i] != 'obo_TStatistic':
            
            erdf[i] = np.linalg.matrix_rank(np.array(conVectors[i]))
            
    return(erdf)

def statsticMap_errorDegreesofFreedom(randomisedir):
    dof_file = os.path.join(randomisedir,
                            'cope1.feat',
                            'stats',
                            'dof')
    
    with open(dof_file, 'r') as input_file:
        dof = input_file.readline()
        dof = dof.split('\n')[0]
        
    return(dof)

def getHeightThreshold_type(randomisedir):
    design_fsl_file = os.path.join(randomisedir,
                                   'design.fsf')

    with open(design_fsl_file, 'r') as input_file:
        lines = input_file.readlines()

    for line in lines:
        if "fmri(thresh)" in line:
            split_line = line.split(' ')
            threshold_type = split_line[-1]
            threshold_type = int(threshold_type.split('\n')[0])

    if threshold_type == 1:
        HeightThreshold = "nidm_PValueUncorrected"
    if threshold_type == 2:
        HeightThreshold = "obo_FWERAdjustedPValue"
    if threshold_type == 3:
        HeightThreshold = "obo_statistic"

    return(HeightThreshold)

def getInference_hasAlternativeHypothesis(randomisedir):
    return("OneTailedTest")
    
# =============================================================================
# Get inference information
# =============================================================================
    
#def getExtentThreshold_clusterSizeInResels(randomisedir):
#    
#    #only set if nidm_ExtentThreshold/prov:type is “obo_statistic"
#    desFsfFile = os.path.join(randomisedir, 'design.fsf')
    

def getSearchSpaceMaskMap_atLocation(randomisedir):
    
    return(os.path.join(
            randomisedir, 'mask.nii.gz'))
    
def getExcursionSetMap_atLocation(randomisedir):
    
    cope_dir = os.path.join(randomisedir, 'cope1.feat')
    tstats = sorted(glob.glob(os.path.join(cope_dir, 'thresh_zstat*.nii.gz')))
    fstats  = sorted(glob.glob(os.path.join(cope_dir,'thresh_zfstat*.nii.gz')))
    
    return(tstats + fstats)



gfeatdir = '/home/tommaullin/Documents/temp3+++.gfeat'
#gfeatdir = '/Users/maullz/Desktop/pytreat_nidmrandomise/level2+.gfeat'

print(getExcursionSetMap_atLocation(gfeatdir))
