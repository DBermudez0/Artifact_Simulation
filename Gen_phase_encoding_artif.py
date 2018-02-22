def Gen_phase_encoding_artif(dname = str, min_disc = int, max_disc = int, slice_num = int):
  '''
  
  Author: Dalton H Bermudez
  
  * >> import Gen_phase_encoding_artif as Gen_artif
  * >> Gen_artif.Gen_phase_encoding_artif(dname = str, min_disc = int, max_disc = int, slice_num = int)
  * >> help(Gen_artif.Gen_phase_encoding_artif)
  ** use help() to see description of function in Python Shell
  
  Purpose: To simulate the motion artifacts encounter in the MRI images. These
  artifacts, unlike the motion artifacts encounter in CT, are based on distortion
  in the k-space rather than in the radon space. The current script can only read
  in 3 dimensional MRI volumes in nii or DICOM files (Zaitsev et al. 2015; Yanasak & Kelly 2014).
  
  Parameters:
  
  dname = path to directory containing original MRI volume.
  
  min_disc = a number indicating the minimum number of lines you want the algorithm
             to discontinue in the phase-encoding direction on the k-space.
             
  max_disc = a number indicating the maximum number of lines you want the algorithm
             to discontinue in the phase-encoding direction on the k-space.
             
  slice_num = a number indicating the slice of 3 dimensional MRI volume you want to
              display.
       
  '''
  
  import numpy as np
  import pandas as pd
  import os
  import nibabel as nib
  import scipy as scp
  import matplotlib.pyplot as plt
  import scipy.fftpack as fftpack
  
  import warnings
  warnings.filterwarnings("ignore")
  
  mri_img = nib.load(dname)
  mri_data = mri_img.get_data()
  mri_data_image = mri_data
  
  a = min_disc
  b = max_disc
  
 
  N = 1
  
  for H in range(0,1):
    # generate N radom numbers in the interval (a,b) with formula:
    # r is the number of lines in the phase-encoding direction that will be discontinue
    r = np.round(a + np.dot((b - a), np.random.rand(N,1)))
    
    c = 0
    d = np.shape(mri_data_image)[0] - 1
    indx = np.round(c + np.dot((d - c), np.random.rand(int(r),1)))
    
    k_space = fftpack.fftn(mri_data_image)
    
    d_1 = np.shape(mri_data_image)[0]
    disc = np.complex(0,0)
    
    for j in range(0, len(indx)):
      for k in range(0, np.shape(mri_data_image)[2]):
        k_space[int(indx[j, :]), : , k] = disc
        
    img_artif = np.abs(fftpack.ifftn(k_space))
    artif_distr = img_artif - mri_data_image
    
    plt.figure(figsize=(10, 4))
    plt.subplot(131)
    plt.imshow(mri_data_image[:,:,slice_num], cmap = 'gray', origin = 'lower')
    plt.title('Real MRI image')
    plt.axis('off')
    plt.suptitle('Simulated Phase encoding based motion artifact with discontinuities of ' + str(int(r)), fontsize=16)
    
    plt.subplot(132)
    plt.imshow(img_artif[:,:,slice_num], cmap = 'gray', origin = 'lower')
    plt.title('Synthesized MRI motion')
    plt.axis('off')
    
    plt.subplot(133)
    plt.imshow(artif_distr[:,:,slice_num], cmap = 'gray', origin = 'lower')
    plt.title('Actual Artifact Distribution')
    plt.axis('off')
    plt.show()
    
  if __name__ == "__Gen_phase_encoding_artif__":
    Gen_phase_encoding_artif(dname = str, min_disc = int, max_disc = int, slice_num = int)
    
        
