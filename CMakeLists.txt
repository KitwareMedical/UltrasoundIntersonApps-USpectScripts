CMAKE_MINIMUM_REQUIRED(VERSION 2.4)
IF(COMMAND CMAKE_POLICY)
  CMAKE_POLICY(SET CMP0003 NEW)
ENDIF(COMMAND CMAKE_POLICY)

PROJECT(UltrasoundSpectroscopyScripts)

find_package( ITK COMPONENTS
  IsotropicWavelets
  ITKFFT 
  ITKCommon
  ITKIOImageBase
  ITKImageGrid
  ITKImageIntensity
  ITKStatistics
  ITKIONRRD
  ITKIOMeta
)
INCLUDE(${ITK_USE_FILE} )

ADD_EXECUTABLE(ReduceLabelImage ReduceLabelImage.cxx )
TARGET_LINK_LIBRARIES (ReduceLabelImage ${ITK_LIBRARIES} )
