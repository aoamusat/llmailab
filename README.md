[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

![GroQ Logo](https://groq.com/wp-content/uploads/2024/03/PBG-mark1-color.svg)

# Computer Vision Chat Pipeline with Groq API Integration

This project implements a computer vision chat pipeline using the Groq API and LangChain framework. It combines image processing capabilities with a language model to analyze visual data and generate responses.

The application processes user input through the Mixtral-8x7b-32768 model, enabling interactive conversations about visual content. It leverages advanced computer vision techniques for tasks such as object detection, classification, and segmentation, while also providing natural language understanding and generation capabilities.

## Repository Structure

- `config.py`: Manages environment variables for LangSmith tracing and API access.
- `helpers.py`: Contains utility functions for interacting with the Groq API.
- `main.py`: Implements the core chat pipeline and user interaction loop.
- `vision.py`: Handles computer vision tasks, including image preprocessing and model inference.

## Usage Instructions

### Installation

1. Ensure you have Python 3.7+ installed.
2. Clone the repository:
   ```
   git clone <repository_url>
   cd <repository_name>
   ```
3. Install the required dependencies:
   ```
   pip install langchain-groq langsmith requests
   ```

### Configuration

1. Create a `.env` file in the project root with the following variables:
   ```
   GROQ_API_KEY=your_groq_api_key
   GROQ_API_URL=https://api.groq.com/v1
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
   LANGCHAIN_API_KEY=your_langchain_api_key
   ```
2. Replace `your_groq_api_key` and `your_langchain_api_key` with your actual API keys.

### Running the Application

Execute the main script to start the chat pipeline:

```
python main.py
```

You will be prompted to enter your input. The application will process it through the Groq API and display the response.

### Using the Computer Vision Features

To utilize the computer vision capabilities:

1. Prepare your image or video files in a supported format (e.g., JPEG, PNG for images; MP4 for videos).
2. Modify the `vision.py` file to load your visual data:
   ```python
   import cv2

   def load_image(path):
       return cv2.imread(path)

   # Example usage
   image = load_image("path/to/your/image.jpg")
   ```
3. Implement the necessary preprocessing and model inference functions in `vision.py`.
4. Integrate the vision processing results with the chat pipeline in `main.py`.

### Troubleshooting

1. API Connection Issues:
   - Error: "Unable to connect to Groq API"
   - Solution: 
     1. Verify your internet connection.
     2. Check that your `GROQ_API_KEY` and `GROQ_API_URL` are correct in the `.env` file.
     3. Ensure the Groq API is not experiencing downtime by checking their status page.

2. Model Loading Errors:
   - Error: "Failed to load model: Mixtral-8x7b-32768"
   - Solution:
     1. Confirm that the model name is correct and available in the Groq API.
     2. Check your API access permissions for the specific model.
     3. Try using a different model by modifying the `model` parameter in `main.py`:
        ```python
        model = ChatGroq(model="alternative-model-name", temperature=0.8)
        ```

3. Environment Variable Issues:
   - Error: "KeyError: 'GROQ_API_KEY'"
   - Solution:
     1. Ensure the `.env` file exists in the project root.
     2. Verify that all required environment variables are set in the `.env` file.
     3. Restart your Python environment to reload the environment variables.

### Debugging

To enable debug mode and verbose logging:

1. Add the following line at the beginning of `main.py`:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```
2. Run the script again to see detailed debug output.

Log files are typically stored in the system's default logging location. On Unix-based systems, check `/var/log/` or `~/.local/share/`.

### Performance Optimization

To optimize performance:

1. Monitor response times using the `time` module:
   ```python
   import time

   start_time = time.time()
   response = pipeline(PROMPT)
   end_time = time.time()
   print(f"Response time: {end_time - start_time:.2f} seconds")
   ```
2. If experiencing slow responses, consider:
   - Reducing the `temperature` parameter in the ChatGroq initialization.
   - Using a smaller or more efficient model if available.
   - Implementing caching for frequent queries.

## Data Flow

The application follows this data flow for processing user inputs and generating responses:

1. User input is received through the command-line interface.
2. The input is passed to the `pipeline()` function in `main.py`.
3. The `ChatGroq` model processes the input using the Groq API.
4. The model's response is returned and displayed to the user.

For visual data processing:

1. Images or video frames are loaded and preprocessed in `vision.py`.
2. Computer vision models analyze the visual data.
3. Results from the vision analysis are integrated with the chat pipeline.
4. The combined information is processed by the language model.
5. The final response, incorporating both visual and textual understanding, is returned to the user.

```
[User Input] -> [main.py] -> [ChatGroq Model] -> [Groq API]
                    ^                                |
                    |                                v
               [vision.py] <- [Image/Video Input]  [Response]
                    |                                |
                    v                                v
            [Vision Processing] -----------------> [Output]
```

Note: Ensure that large files or sensitive data are not processed directly through the API. Instead, consider using secure file handling and data summarization techniques when dealing with visual content.