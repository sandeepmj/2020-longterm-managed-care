# Delays in Homecare Decisions for Alzheimer’s and Dementia Patients in New York State

This data journalism project investigates how long the New York State Department of Health takes to determine the number of homecare hours granted to patients diagnosed with Alzheimer's disease or dementia.

## Byline and Credits

**By:** Sandeep Junnarkar  
**Affiliation:** WNYC
**Date:** 2020

---

## Project Summary

The NYS Health Department released a series of determination letters in PDF format in response to a records request. Each letter contains the date the application was received and the date a final decision was issued. Using custom parsing and analysis, we extracted these dates to calculate delays in care decisions for individuals with cognitive impairments.

---

## Data Sources

- **Homecare Determination Letters (PDFs)**  
  Source: New York State Department of Health  
  Access method: FOIL request  
  Files located in `/pdfs/` folder  
  Approximate volume: XX documents, spanning [Year-Year]

---

## Methodology

1. **PDF Extraction**  
   Used a combination of PDF parsing libraries (e.g., `PyMuPDF`, `pdfplumber`, or `pdfminer.six`) to extract structured text.

2. **Date Identification**  
   Applied regular expressions and pattern matching to identify:
   - **Application Received Date**
   - **Decision Date**

3. **Eligibility Filter**  
   Filtered letters for patients explicitly diagnosed with Alzheimer’s or dementia (via keyword search and contextual parsing).

4. **Delay Calculation**  
   Computed time between application and decision for each relevant case.

5. **Analysis**  
   Generated summary statistics (e.g., average delay, longest wait) and categorized results by diagnosis and year.

All analysis steps are documented in the `notebooks/` and `scripts/` folders.

---

## How to Reproduce This Analysis

1. Clone this repository:
   
   git clone https://github.com/yourusername/homecare-delays-ny.git
