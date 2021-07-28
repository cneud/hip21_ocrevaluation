# hip21_ocrevaluation

Resources for replication of the experiments in the [HIP'21](https://blog.sbb.berlin/hip2021/) paper "A Survey of OCR Evaluation Tools and Metrics".  

## How to use

TODO: Makefile and documentation

## Data

The `data` directory contains the Ground Truth, OCR and evaluation results. 

All files are named by their unique 8-digit [PRImA-ID](https://www.primaresearch.org/datasets) followed by one or a combination of the following extensions:  
* `gt` for Ground Truth (PAGE-XML)
* `gt4hist` for OCR results using [GT4HistOCR](https://github.com/tesseract-ocr/tesstrain/wiki/GT4HistOCR) model (ALTO)
* `deu`, `eng`, `est`, `fin`, `fra`, `lav`, `nld`, `pol`, `swe` for OCR results using [tessdata](https://github.com/tesseract-ocr/tessdata) models (ALTO)
* `conf` for [OCR confidence](https://github.com/cneud/alto-ocr-confidence) scores (TXT)
* `dinglehopper` for [dinglehopper](https://github.com/qurator-spk/dinglehopper) CER/WER report (JSON)
* `ocrevalUAtion` for [ocrevalUAtion](https://github.com/impactcentre/ocrevalUAtion) CER/WER/BoW report (HTML)
* `ocrevalCER` for [ocreval](https://github.com/eddieantonio/ocreval) CER report (TXT)
* `ocrevalWER` for [ocreval](https://github.com/eddieantonio/ocreval) WER report (TXT)
* `primaCER` for [PRImA](https://www.primaresearch.org/tools/PerformanceEvaluation) CER report (CSV)
* `primaWER` for [PRImA](https://www.primaresearch.org/tools/PerformanceEvaluation) WER report (CSV)
* `primaBoW` for [PRImA](https://www.primaresearch.org/tools/PerformanceEvaluation) BoW report (CSV)

TODO: PRImA Layout evaluation results

## How to cite
```bibtex
@inproceedings{DBLP:conf/icdar/Neudecker2021hip,
author    = {Clemens Neudecker and
             Konstantin Baierer and 
             Mike Gerber and
             Christian Clausner and
             Apostolos Antonacopoulos and
             Stefan Pletschacher},
title     = {A Survey of OCR Evaluation Tools and Metrics},
booktitle = {Proceedings of the 6th International Workshop on Historical Document Imaging and 
             Processing (HIP'21), Lausanne, Switzerland, September 6, 2021},
publisher = {{ACM}},
year      = {2021},
url       = {https://dl.acm.org/conference/hip/proceedings}
}
```
