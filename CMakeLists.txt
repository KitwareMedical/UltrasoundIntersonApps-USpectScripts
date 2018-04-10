CMAKE_MINIMUM_REQUIRED(VERSION 2.4)
IF(COMMAND CMAKE_POLICY)
  CMAKE_POLICY(SET CMP0003 NEW)
ENDIF(COMMAND CMAKE_POLICY)

PROJECT(UltrasoundSpectroscopyScripts)

find_package( ITK COMPONENTS
  Ultrasound
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

ADD_EXECUTABLE(ButterworthBandpass ButterworthBandpass.cxx )
TARGET_LINK_LIBRARIES (ButterworthBandpass ${ITK_LIBRARIES} )

ADD_EXECUTABLE(BMode BMode.cxx )
TARGET_LINK_LIBRARIES (BMode ${ITK_LIBRARIES} )
