FIELDLIST = ["packetSize","seqNum","timeStamp","currentSampleOffset","column","row","useOffset","readSft","serialID","numBlocks","triggerMask","sampleOffset","partialNumSamples","sampleDelay","staleData","numBlocksDigitized","totalNumSamples","triggerDelay","blockID","sablockID","seqTime","value","cvalue","cstd"]

CHSTRUCT = "struct chID_t {Int_t packetSize; Int_t seqNum;Float_t timeStamp;Int_t currentSampleOffset;Int_t column;Int_t row;Int_t useOffset;Int_t readSft;Int_t serialID;Int_t numBlocks;Int_t triggerMask;Int_t sampleOffset;Int_t partialNumSamples;Int_t sampleDelay;Int_t staleData;Int_t numBlocksDigitized;Int_t totalNumSamples;Int_t triggerDelay;Int_t blockID;Int_t sablockID;Int_t seqTime;Int_t value;Float_t cvalue;Float_t cstd; };"

CHBRANCH = "packetSize/I:seqNum:timeStamp:currentSampleOffset:column:row:useOffset:readSft:serialID:numBlocks:triggerMask:sampleOffset:partialNumSamples:sampleDelay:staleData:numBlocksDigitized:totalNumSamples:triggerDelay:blockID:sablockID:seqTime:value:cvalue/F:cstd/F"

