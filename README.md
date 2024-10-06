FINAL DEMO:

https://jade-crepe-b4516a.netlify.app/

DATA SOURCE: https://www.spaceappschallenge.org/nasa-space-apps-2024/challenges/seismic-detection-across-the-solar-system/?tab=resources
Space Apps 2024 Seismic Detection Data Packet:
lunar & mars

A “lunar” subfolder containing:
Training data (in miniseed and CSV format) for Grade A lunar events from Apollo 12, a seismic catalog, and plots.
A test dataset (in miniseed and CSV format) using Grade A and B data from Apollo 12, 15, and 16
A “mars” subfolder containing:
Training data (in miniseed and CSV format) for two events recorded for InSight, a seismic catalog, and plots.
A test dataset (in miniseed and CSV format) for Mars InSight events occurring from 2019-2022.

IA4SPACE

Summary
When transmitting seismic data back to Earth, planetary missions must contend with high power requirements. Developing on-board algorithms for lander-side signal analysis improves telemetry priority by filtering and selecting just the most important seismic data for transmission. Programming such algorithms explicitly can be tricky, especially when there is no prior seismic data for the planetary body. In our project, we tackled this issue by using a combination of signal processing and machine learning approaches to recognize seismic occurrences from raw data. To begin, we used a Fourier transform to analyze the frequency pattern in the seismic data, which allowed us to distinguish between noise and real seismic signals. We then developed a high-pass filter to remove low-frequency noise while retaining the important high-frequency components required for accurate event identification. Following this preprocessing stage, we trained an XGBoost model, a sophisticated machine learning method, to categorize the filtered data as seismic events or non-events. This enabled the model to generalize seismic signal properties and forecast occurrences with high accuracy, despite the lack of sufficient training data from the planetary body. We explored various machine learning models and configurations, including base models, random oversampling, SMOTE, random undersampling, threshold adjustment, random forest, and XGBoost. These models were evaluated on accuracy, precision, recall, and F1 score metrics. The XGBoost model achieved the highest accuracy of 88.15%, demonstrating a strong balance between precision (78.43%), recall (88.89%), and F1 score (83.33%). Our results showed that the XGBoost model was the best fit for lunar seismic detection, outperforming other models, including random forest and threshold-adjusted models, which struggled due to class imbalance and overfitting.

Methodology
Overview of methodologies employed, including data preprocessing, machine learning model development, and evaluation techniques.

A. Data Preprocessing
Catalog Data Overview The dataset used for this project is the Apollo 12 Grade A catalog data. This dataset contains detailed information about seismic activity recorded on the Moon.

B. Separate Signal from Noise (Filtering Strategy)
Algorithm Development: The predictive algorithm leverages machine learning techniques to forecast seismic events. 
Fourier Transform:  We apply the Fourier Transform to analyze the frequency components of the seismic signals, allowing us to identify dominant frequency ranges that correlate with seismic events. 3.2.2 Wavelet Transform Wavelet analysis provides time-frequency localization, helping us detect transient seismic events more accurately and understand their evolution over time




Windowing and Feature Extraction for Model Training
The filtered seismic signal is divided into fixed-size windows (e.g., 60 seconds), where each window represents a sequence of seismic measurements. This allows us to capture local temporal patterns related to seismic events. Feature Extraction: From each window, features such as velocity mean, variance, and standard deviation are computed to describe the characteristics of the seismic data. These features are then used to train the model.

C. Machine Learning model selection & Hyperparametrization
Training the Model
Model Training: Using the extracted features from both event and non-event windows, the XGBoost model is trained to classify windows as either containing a seismic event or not. The model is designed to handle imbalanced data and efficiently learns from complex patterns in the seismic signal. Cross-Validation: To ensure model robustness, cross-validation is performed during training to prevent overfitting and to validate the model’s performance across different folds of the data.

Model Evaluation

The XGBoost model performed the best with an accuracy of 88.15% and demonstrated a strong balance between precision, recall, and F1 score. The random forest model achieved reasonable accuracy (66.67%), but failed in recall due to an imbalance in the dataset, resulting in poor prediction of class 1. Models that employed random oversampling, SMOTE, and undersampling showed lower accuracies, likely due to overfitting or biased class predictions.

Energy saving
Signals over long distances are costly and require considerable energy. These signals are often contaminated with noise so, to optimize the quality of the transmitted data and reduce the energy cost of transmission, filtering techniques are employed to remove noise and preserve 9 only the relevant information. A custom code was developed to analyze the energy savings achieved by applying different filtering techniques to seismic signals.

D.Results interpretation
The results from the custom code show a significant reduction in energy usage across the 15 analyzed samples. The mean energy savings of 84.15% indicates that the filtering techniques are highly effective in reducing unnecessary noise components from the signals. In particular, the high-pass filter was instrumental in removing lower frequency noise, resulting in substantial energy savings. The data highlights that the most relevant seismic information resides in higher frequencies, while the band-pass filter ensures that the signal’s critical information is preserved, even while 11 achieving savings close to 90%.

Practical impact 
The implementation of these filters has direct implications for the operation of seismic monitoring systems on the Moon. Since transmissions from the Moon to Earth require a large amount of energy, the ability to reduce over 80% of the energy associated with signal transmission not only reduces costs but also extends the lifespan of lunar seismic sensors, which often operate in environments where energy availability is limited. Moreover, the use of filtering techniques allows optimizing subsequent analysis of the signals on Earth by providing cleaner and more focused data on important events, facilitating better interpretation of the seismic phenomena occurring on the Moon.

Conclusion
In conclusion, the use of high-pass and band-pass filters in seismic signals from the Moon, analyzed through a custom code on a sample of 15 lunar seismic signals, has proven to be a highly effective technique for reducing energy consumption. With an average energy savings of 84.15%, this method shows that it is possible to significantly improve the efficiency of data transmission systems without sacrificing the quality of critical information. Future research could explore the implementation of adaptive algorithms that dynamically adjust the filter parameters based on environmental conditions or detected events.
Principal Insights of our solutions:
1. Filtering contributed to energy savings in signal classification.
2. Temporal and Spatial Patterns Enhance Detection Accuracy.
3. Low-Frequency Ranges Capture Predictive Seismic Signals More Effectively (between 0.5 – 1.5 HZ)
4. Best Performance wiht XGBoost algorithms. XGBoost Excels in Handling Imbalanced Data with Superior Performance

Scalability of our solution
The detection of seismic activity on the Moon and Mars offers numerous applications and advantages for both scientific research and future space exploration. Here are some key benefits:
Mission Safety: Detecting seismic events can protect space missions by identifying potential risks, such as quakes or surface instability, which could endanger equipment or astronauts.
Planetary Structure Understanding: Seismic data provides critical insights into the internal composition and structure of the Moon and Mars, such as the size of their cores, mantle properties, and crust thickness, contributing to our knowledge of planetary formation.
Building Stable Infrastructure: For future lunar or Martian bases, seismic monitoring is essential to select safe construction sites and develop infrastructure capable of withstanding quakes or underground shifts.
Resource Exploration: Seismic detection can help locate underground resources like water or minerals, vital for sustainable human presence and resource utilization on these celestial bodies.
Preparation for Human Habitation: Understanding seismic patterns is crucial for planning human settlements, ensuring that habitats are built in stable areas, and minimizing exposure to potential natural hazards.
Enhancing Earthquake Prediction Techniques: Seismic detection on the Moon and Mars can improve machine learning models for earthquake prediction on Earth by providing comparative data on how different planetary environments influence seismic activity.
Advanced AI and Machine Learning Applications: Utilizing AI and machine learning models enhances the accuracy of seismic detection, filtering out noise and improving real-time predictions, making these technologies indispensable for future exploration missions.
Detection Technology: Tech firms can create and sell specialized devices and sensors for detecting seismic activity on other planets.
Climate Change Research: Understanding the impact of seismic events on the atmospheres and surfaces of Mars and the Moon to model conditions for potential colonization.
Integrate with other demo projects from previous competitions, allowing for a more comprehensive and robust approach to space exploration challenges. This adaptability ensures that our system can work in tandem with various innovations, creating a unified framework for future planetary missions.
These applications highlight how seismic detection is not only pivotal for safety but also for the broader goal of expanding human presence beyond Earth.




TECHNICAL INFORMATION:
Here’s a description of the necessary libraries you mentioned, along with their purpose and usage in the context of data analysis and machine learning, particularly for seismic signal analysis:

### 1. **ObsPy**
- **Description**: ObsPy is a Python library designed for the programming and analysis of seismic data. It provides tools for handling, processing, and visualizing seismic data in various formats.
- **Usage**: It is commonly used to read data from seismic stations, perform signal transformations (such as filtering), and calculate correlation functions and frequency spectra. Its capability to efficiently manage seismic data makes it a valuable tool for researchers in the field of seismology.

### 2. **XGBoost**
- **Description**: XGBoost is a machine learning library that implements gradient boosting algorithms. It is highly efficient, flexible, and portable, making it popular in data science competitions.
- **Usage**: It is used for classification and regression tasks, especially in imbalanced datasets. Its ability to handle missing data and perform regularization allows it to achieve superior performance in detecting seismic events from features extracted from signals.

### 3. **Pandas**
- **Description**: Pandas is a data analysis library that provides flexible and powerful data structures, such as DataFrames and Series.
- **Usage**: It is used for data manipulation and analysis, enabling the loading, cleaning, transforming, and analyzing of tabular data. In the context of seismic analysis, it is used to organize seismology data and facilitate feature extraction and statistical analysis.

### 4. **Matplotlib**
- **Description**: Matplotlib is a plotting library in Python. It allows for the creation of static, animated, and interactive visualizations.
- **Usage**: It is used to visualize seismic data, create frequency graphs, spectra, and any type of graphical representation that aids in interpreting the results of seismic analysis.

### 5. **Joblib**
- **Description**: Joblib is a library that facilitates the serialization of Python objects and the parallel execution of processes.
- **Usage**: It is used to save and load machine learning models, as well as to execute tasks in parallel, improving the efficiency of data processing and training models on large datasets.

### 6. **JSON**
- **Description**: JSON (JavaScript Object Notation) is a lightweight data interchange format that is easy for humans to read and write, and for machines to parse and generate.
- **Usage**: It is used to store and transport structured data, such as configurations or analysis results. In the context of seismic analysis, it can be useful for handling metadata or intermediate results in a structured format.

### 7. **PyWavelets (pywt)**
- **Description**: PyWavelets is a library for wavelet analysis and wavelet transformations in Python.
- **Usage**: It is used to perform wavelet transformations on data, which is useful for analyzing transient signals and detecting seismic events. It allows for the decomposition of signals into different scales and frequencies, facilitating the identification of patterns and characteristics in seismic data.

### Summary
These libraries form a powerful set of tools for the manipulation, analysis, and visualization of seismic data. The combination of signal processing capabilities (ObsPy, PyWavelets) and machine learning techniques (XGBoost), along with data manipulation and analysis (Pandas), as well as visualization (Matplotlib), allows for effectively addressing the challenges in seismic signal analysis.

If you need more details about any of these libraries or how to use them, just let me know!
