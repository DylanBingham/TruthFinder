# README.txt

## DESCRIPTION
TruthFinder is a cutting-edge web-based application built to evaluate and visualize the credibility of articles using advanced natural language processing techniques and a random forest model that achieved 94% accuracy on a holdout test dataset. By analyzing textual elements, the platform calculates detailed metrics—including tf-idf terms, polarity, subjectivity, readability, speech attributes, and word count—to offer users a nuanced understanding of the content at hand. These metrics help reveal the underlying tone and style of a piece, distinguishing between truthful reporting and content laden with opinions or bias.
Beyond raw metrics, TruthFinder enhances data interpretation through interactive visualizations such as kernel density plots. These visual tools allow users to observe the distribution of credibility metrics across different articles, making it easier to spot trends and outliers. The intuitive interface not only simplifies the exploration of complex data but also engages users by enabling them to dynamically compare pieces of content, fostering a deeper insight into how various textual features contribute to overall credibility.
At its core, TruthFinder is designed to empower users with the ability to critically assess the reliability of digital content. By blending robust analytics with dynamic visual representations, the application promotes media literacy and informed decision-making in a landscape often cluttered with misinformation. This integrated approach supports the overarching mission of enhancing transparency and trust in information, ultimately guiding users to discern fact from opinion in their daily media consumption.

## INSTALLATION
1. Optionally, clone the repository:
   ```
   git clone https://github.com/DylanBingham/TruthFinder
   cd TruthFinder
   ```

   Or simply unzip the code into a local directory.

2. Install the required dependencies:
   - Ensure you have Python 3.8+ installed.
   - Create a virtual environment:
     ```
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```
       venv\Scripts\activate
       ```
     - On macOS/Linux:
       ```
       source venv/bin/activate
       ```
   - Install the dependencies:
     ```
     pip install -r requirements.txt
     ```

## EXECUTION
1. Launch the application:
   - Start the backend server by typing `python app.py` into your terminal from the root directory of the project.
   - Visit the default local host (it is recommended to use microsoft edge at 100% zoom) of flask http://127.0.0.1:5000/
    - If you have any errors you may want to check if the 5000 port is already occupied on your machine.

2. Analyze an article:
   - Select an article from the dropdown menu or input a URL.
   - Click the "Save" button to analyze the article.

3. View results:
   - The analysis results, including metrics and visualizations, will be displayed in the "Analysis Results" section.

4. Explore visualizations:
   - Interact with the charts to understand the article's credibility, sentiment, and subjectivity.
   - Try hovering over the different labels and objects within the charts.
   - You can explore more detailed information about the components of the application by clicking the green
   info button.

For further assistance, refer to the inline comments in the codebase or the documentation provided in the repository.