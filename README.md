
# Face Recognition Attendance System

The Face Recognition Attendance System is a Python-based project that automates the attendance-taking process using facial recognition technology. This system captures and identifies faces from live video streams or images, marking attendance for recognized individuals in real-time. After marking attendance, it announces the completion via a voice module.


## Features

- **Real-time Face Recognition:** Identifies and marks attendance for individuals using facial recognition.
- **Voice Feedback:** Announces attendance confirmation using a voice module.
- **Data Storage:** Saves attendance records in a CSV file.
- **Streamlit Interface:** Displays attendance data in a user-friendly interface.


## Requirements 

To run this project, you need the following Python libraries:

```Python 3.x
OpenCV
NumPy
dlib or face_recognition library
pandas (for data handling)
```
- streamlit (for the web interface)

## Setup & Installation

1. Clone the Repository

```bash
 git clone https://github.com/your-username/Face-Recognition-Attendance-System.git
 cd Face-Recognition-Attendance-System

```
2. Install Required Libraries
Create a virtual environment and install the necessary libraries:
```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
```
***Note:*** If requirements.txt is not provided, you can manually install the required packages:
```bash
pip install opencv-python numpy dlib pandas face_recognition streamlit
```
3. Set Up the Project
- Ensure you have the Haar Cascade file (haarcascade_frontalface_default.xml) in the project directory.
- Place your dataset images in the data directory.
- Run add_faces.py to add faces to the recognition system.

4. Run the Application
To start the attendance system, execute:
```bash
python app.py
```

To view the attendance data in the Streamlit interface, execute:

```bash
streamlit run app.py

```

## Usage 

1. **Add Faces:** Run add_faces.py to add images of individuals to the system.
2. **Start Attendance System:** Run app.py to start capturing video and marking attendance.
3. ***View Attendance:*** Access the Streamlit app to view the attendance records.


## Contributing

Contributions are always welcome!

Feel free to fork the repository and make changes. For major updates or contributions, please open an issue or submit a pull request.

Please adhere to this project's `code of conduct`.

