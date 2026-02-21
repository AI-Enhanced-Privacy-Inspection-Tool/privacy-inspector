import os
import platform

# TODO: maybe only use Windows since macOS or Linux can't be tested easily
def get_app_data_dirs():
    """
    Returns a list of application data directories based on the operating system.
    On Windows, it returns both APPDATA and LOCALAPPDATA.
    """
    
    print("Finding app data directories...")
    system = platform.system()

    if system == 'Windows':
        app_data = os.getenv('APPDATA') 
        local_app_data = os.getenv('LOCALAPPDATA') 
        print(f"Windows APPDATA: {app_data}, LOCALAPPDATA: {local_app_data}")
        return [app_data, local_app_data]
    elif system == 'Darwin':  # macOS
        home = os.path.expanduser('~')
        return [os.path.join(home, 'Library', 'Application Support')]
    else:  # Linux and other Unix-like systems
        home = os.path.expanduser('~')
        return [os.path.join(home, '.config'), os.path.join(home, '.local', 'share')]

    
if __name__ == "__main__":
    dirs = get_app_data_dirs()