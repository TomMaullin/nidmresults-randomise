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

gfeatdir = '/home/tommaullin/Downloads/level2.gfeat'

print(getNeuroImagingAnalysisSoftwareType(gfeatdir))
print(getNeuroimagingAnalysisSoftware_softwareVersion(gfeatdir))
