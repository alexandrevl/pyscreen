# PyScreen - Advanced Screen Recording Analyzer

Harness the power of AI with PyScreen, a state-of-the-art tool designed to extract, analyze, and visualize pertinent information from screen recording videos. Built upon advanced computer vision, text processing, and artificial intelligence techniques, PyScreen transforms your screen recordings into data-rich insights.

## Key Features

- **Screen Extraction:** Seamlessly extracts data from the screens of any given video file.

- **Word Cloud Generation:** Generates dynamic word clouds reflecting the most frequently used words in your screens, offering a quick content overview.

- **Color Analysis:** Identifies the dominant color schemes prevalent in your screens, providing a snapshot of aesthetic and design choices.

- **GPT Analysis:** Employs OpenAI's GPT-4 model to generate human-like text descriptions based on word data extracted from screens, enhancing content understanding and discoverability.

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/alexandrevl/pyscreen.git
   ```

2. Navigate to the project directory:

   ```bash
   cd pyscreen
   ```

3. Run PyScreen on your preferred screen recording:

   ```bash
   python main.py --input your_screen_recording.mp4
   ```

## Required Libraries

PyScreen relies on the following Python libraries:

- `gc` for optimal memory management
- `json` and `pandas` for effortless data manipulation
- `cv2` (opencv) for comprehensive image processing
- `pytesseract` for OCR functionality
- `nltk` for advanced text processing
- `WordCloud` for crafting visually compelling word clouds
- `openai` for utilizing the GPT-4 model
- `python-dotenv` for storing sensitive information
- `unidecode` for handling Unicode characters

Ensure these dependencies are installed prior to running PyScreen. You can install them using pip:

```bash
pip install opencv-python pytesseract nltk wordcloud openai pandas python-dotenv unidecode
```

To use chatGPT functionality, you must have an OpenAI API key. You can obtain one [here](https://beta.openai.com/). Once you have your API key, create a `.env` file in the project directory and add the following line:

```bash
OPENAI_API_KEY=your_api_key
```

Additionally, Tesseract OCR needs to be installed on your system. Follow this [guide](https://tesseract-ocr.github.io/tessdoc/Installation.html) for detailed installation instructions.

## Contribution

Your contributions matter! Feel free to submit a pull request to augment the functionality and usability of PyScreen.

## License

PyScreen is open-source software, licensed under the terms of the MIT license. Feel free to share, modify, and distribute.
