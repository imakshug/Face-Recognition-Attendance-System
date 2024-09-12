
# Automating Bank Cheque Extraction from Scanned Documents

This project, Automating Bank Cheque Extraction from Scanned Documentss, aims to develop an automated pipeline that extracts and processes cheque details from scanned PDF documents. It uses OCR (Optical Character Recognition) technologies to recognize key information from cheque images, such as:


- Bank name
- Cheque number
- Account holder’s name
- IFSC code
- MICR code
- Amount
- Date of issuance



## Features

- Automated Cheque Extraction: Extracts essential information from scanned cheque PDFs.
- Batch Processing: Supports processing multiple PDF files at once.
- Data Export: Saves extracted data in CSV or Excel format for easy analysis.
- Graphical User Interface (GUI): Provides a simple interface to run the application.
- Logging & Error Handling: Logs the process and captures any errors for review.
## Installation

### Prerequisites
- Python 3.8 or above
- Tesseract OCR
- Libraries from requirements.txt

Steps
1. Clone the repository:
```bash
 git clone https://github.com/yourusername/Automating-Bank-Cheque-Extraction.git
 cd Automating-Bank-Cheque-Extraction

```
2. Install dependencies:
```bash
   pip install -r requirements.txt
```   
3. [Install Tesseract OCR](https://github.com/tesseract-ocr/tesseract):


4. Add Tesseract to your system PATH.
## Usage/Examples
### Running the Extraction Script
1. Place the scanned PDF files in the data/ folder.

2. Run the main script:
```python
python src/main.py --input data/cheque.pdf --output output/extracted_data.csv

```

3. You can also use the GUI:
```python
python src/gui.py
```

### Output
The extracted cheque information will be stored in output/extracted_data.csv and output/extracted_text.xlsx.
## Technology Stack


**Python:** Core language for development.

**Tesseract OCR:** For text recognition from scanned cheque images.

**OpenCV:** For image preprocessing.

**PyPDF2 / pdfplumber:** For PDF handling and extraction.

**Regex:** For pattern matching of cheque data.

**Pandas:** For organizing and storing the extracted data.


## License

This project is licensed under the MIT License - see the [License](https://choosealicense.com/licenses/mit/) file for details.


## Contributing

Contributions are always welcome!

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Commit your changes (git commit -m 'Add new feature').
4. Push the branch (git push origin feature-branch).
5. Open a pull request and describe the changes in detail.


Please adhere to this project's `code of conduct`.

