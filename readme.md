# WallPair Project

This is the WallPair project, a Django web application where user can upload two pictures as poll and other users can react on it via likes and comments.It also uses youtube api for youtube related posts

## Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/wallpair.git
    ```

2. Navigate to the project directory:

    ```bash
    cd wallpair
    ```

3. Create a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows:

    ```bash
    venv\Scripts\activate
    ```

    - On macOS and Linux:

    ```bash
    source venv/bin/activate
    ```

5. Install the project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. Configure the settings:

    - Copy the `example_settings.py` file to `settings.py`:

    ```bash
    cp wallpair/settings/example_settings.py wallpair/settings/settings.py
    ```

    - Modify `wallpair/settings/settings.py` as needed, adding your database, API keys, and other configuration.

2. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

## Running the Application

1. Run the development server:

    ```bash
    python manage.py runserver
    ```

2. Access the application in your web browser at `http://127.0.0.1:8000/`.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and create a pull request.


