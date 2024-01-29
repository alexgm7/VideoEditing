# VideoEditing

Video splitter for shared dropbox folder or local videos

## Usage

1. Install pip requirements

```bash
pip install -r requirements.txt
```

2. Modify values in config.yaml
Access token is only needed if you want to download folders from dropbox

```bash
ACCESS_TOKEN: "placeholder"
database: ""
user: ""
pass: ""
host: ""
port: 
```

2.1 Create Access token from Dropbox:
    a - Use this link to create a new app (https://www.dropbox.com/developers/apps/create). 
    b - Modify the Permissions in the corresponding tab and check all the "*.read* boxes for Files and Folders.
    c - Click Submit
    d - Create a new token in the Settings tab.

3. Run the main script "clipvideos.py" with python

    Example:

    ```bash
    python clipvideos.py --target_folder "C:\Users\Desktop\Notebooks\videos"    
    ```

    The previous command will search for a ".mp4" file in the target_folder and split it in clips of 60 seconds.

    ```bash
    python clipvideos.py --target_folder "C:\Users\Desktop\Notebooks\videos"   --url "https://www.dropbox.com/sh/..." 
    ```

    The previous command will download the ".mp4" file inside the dropbox folder in the given target_folder and then process it.

    NOTES: Currenlty only working with one ".mp4" file per folder. Multiple files still in progress.
    You can also use ".zip" files.

    