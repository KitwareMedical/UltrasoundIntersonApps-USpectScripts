
#include <tclap/CmdLine.h>
#include "ImageIO.h"

#include "itkImage.h"
#include "itkImageRegionIteratorWithIndex.h"
#include "itkMetaDataObject.h"

int main(int argc, char **argv ){

  //Command line parsing
  TCLAP::CmdLine cmd("Convert Label Image to Numpy", ' ', "1");

  TCLAP::ValueArg<std::string> lArg("l","label","Label Image", true, "",
      "filename");
  cmd.add( lArg );

  TCLAP::ValueArg<std::string> sArg("s","spectra","Spectra image", true, "",
      "filename");
  cmd.add( sArg );

  try{
    cmd.parse( argc, argv );
  }
  catch (TCLAP::ArgException &e){
    std::cerr << "error: " << e.error() << " for arg " << e.argId() << std::endl;
    return -1;
  }
  const unsigned short mixedClass = 10;

  typedef itk::Image< unsigned short, 2> LabelImageType;
  LabelImageType::Pointer labelImage = ImageIO<LabelImageType>::ReadImage( lArg.getValue() );
  LabelImageType::SizeType labelImageSize = labelImage->GetLargestPossibleRegion().GetSize();

  typedef itk::Image< float, 2> ImageType;
  ImageType::Pointer spectraImage = ImageIO<ImageType>::ReadImage( sArg.getValue() );

  //Does not seem to work
  //const itk::MetaDataDictionary & dict = spectraImage->GetMetaDataDictionary();
  unsigned int fft1DSize = 128;
  //itk::ExposeMetaData< unsigned int >( dict, "FFT1DSize", fft1DSize );

  std::cout << fft1DSize << std::endl;

  LabelImageType::Pointer labelImageReduced = LabelImageType::New();
  labelImageReduced->CopyInformation( spectraImage );
  labelImageReduced->SetNumberOfComponentsPerPixel(1);
  labelImageReduced->SetRegions( spectraImage->GetLargestPossibleRegion() );
  labelImageReduced->Allocate();
  labelImageReduced->FillBuffer( 0 );



  typedef itk::ImageRegionIteratorWithIndex< ImageType > ImageIterator;
  ImageIterator spectraImageIt( spectraImage, spectraImage->GetLargestPossibleRegion() );

  ImageType::PointType point;
  LabelImageType::IndexType labelIndex;
  //LabelImageType::IndexType labelIndexRe;
  while( ! spectraImageIt.IsAtEnd() ){
    ImageType::IndexType index = spectraImageIt.GetIndex();
    spectraImage->TransformIndexToPhysicalPoint(index, point);
    labelImage->TransformPhysicalPointToIndex(point, labelIndex);
    //labelImageReduced->TransformPhysicalPointToIndex(point, labelIndexRe);
    //std::cout << labelIndex << std::endl;
    //std::cout << index << std::endl;
    //std::cout << labelIndexRe << std::endl << std::endl;

    labelImageReduced->SetPixel( index, labelImage->GetPixel( labelIndex ) );
    /*
    std::vector<int> classes(5, 0);
    int lower =  std::max(0, (int) ( labelIndex[0] - fft1DSize / 2));
    int upper =  std::min((int)labelImageSize[0], (int) (labelIndex[0] + fft1DSize/2));
    for(int i = lower; i < upper; i++){
       labelIndex[0] = i;
       classes[ labelImage->GetPixel(labelIndex) ] += 1;
    }
    int maxClassCount = 0;
    unsigned short maxClassIndex = 0;
    for(unsigned short i=0; i<classes.size(); i++){
      if( maxClassCount < classes[i] ){
        maxClassCount = classes[i];
        maxClassIndex = i;
      }
    }
    //std::cout << maxClassIndex <<": " << maxClassCount << " | " << labelImage->GetPixel(index)  << std::endl;

    if( maxClassCount > ( (upper-lower) * 0.75 ) ){
      labelImageReduced->SetPixel( index, maxClassIndex );
    }
    else{
      labelImageReduced->SetPixel( index, mixedClass );
    }
    */

    ++spectraImageIt;
  }

  std::string filepath = lArg.getValue();
  filepath.insert( filepath.length()-4, "-reduced");
  std::cout << filepath << std::endl;
  ImageIO<LabelImageType>::saveImage( labelImageReduced, filepath );

}


