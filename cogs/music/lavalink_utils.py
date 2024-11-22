import threading
import subprocess
import os
import requests
import yaml

class LavalinkManager:
    def __init__(self, ip_address : str, port : int, password : str, application_yml_path : str = "application.yml", lavalink_file_path : str = "Lavalink.jar"):
        # Config variables
        self.ip_address : str = ip_address
        self.port : int = port
        self.password : str = password
        self.application_yml_path : str = application_yml_path
        self.lavalink_file_path : str = lavalink_file_path

        created_application_yml = self.__create_application_yml()
        assert created_application_yml, "[LavalinkManager] Failed to create application.yml file."
        downloaded_lavalink = self.__download_lavalink()
        assert downloaded_lavalink, "[LavalinkManager] Failed to download Lavalink.jar."
        
        # Threading variables
        self.process = None
        self.thread = None

    def start_lavalink(self):
        # Thread target function
        def run_lavalink():
            # Start Lavalink using subprocess, storing the process object
            self.process = subprocess.Popen(
                ['java', '-jar', 'Lavalink.jar'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # Wait for Lavalink to complete (this keeps the thread alive)
            self.process.communicate()

        # Create a thread that will run Lavalink
        self.thread = threading.Thread(target = run_lavalink)
        self.thread.start()

    def stop_lavalink(self):
        # Stop Lavalink by sending a termination signal
        if self.process:
            self.process.terminate()  # Gracefully terminate
            self.thread.join()        # Wait for the thread to finish
            print("Lavalink process stopped.")

    def __download_lavalink(self) -> bool:        
        if os.path.exists(self.lavalink_file_path):
            os.remove(self.lavalink_file_path)

        lavalink_repo_url = "https://api.github.com/repos/lavalink-devs/Lavalink/releases/latest"
        response = requests.get(lavalink_repo_url)
        lavalink_latest_version = response.json()["name"]
        download_url = f"https://github.com/lavalink-devs/Lavalink/releases/download/{lavalink_latest_version}/Lavalink.jar"

        download_request = requests.get(download_url)
        file = open(self.lavalink_file_path, 'wb')
        for chunk in download_request.iter_content(10**5):
            file.write(chunk)
        file.close()

        downloaded_size = os.path.getsize(self.lavalink_file_path)
        goal_size = response.json()["assets"][0]["size"]

        return os.path.exists(self.lavalink_file_path) and downloaded_size == goal_size

    def __create_application_yml(self) -> bool:
        if os.path.exists(self.application_yml_path):
            os.remove(self.application_yml_path)

        youtube_plugin_repo_url = "https://api.github.com/repos/lavalink-devs/youtube-source/releases/latest"
        response = requests.get(youtube_plugin_repo_url)
        youtube_plugin_latest_version = response.json()["name"]
        youtube_plugin_latest_version = "1.8.2"

        base_application_path = "./cogs/music/base_application.yml"

        with open(base_application_path) as f:
            yaml_content = yaml.safe_load(f)

        yaml_content["server"]["port"] = self.port
        yaml_content["server"]["address"] = self.ip_address
        yaml_content["lavalink"]["server"]["password"] = self.password
        yaml_content["lavalink"]["plugins"][0]["dependency"] = f"dev.lavalink.youtube:youtube-plugin:{youtube_plugin_latest_version}"

        with open(self.application_yml_path, "w") as f:
            yaml.dump(yaml_content, f)
        
        return os.path.exists(self.application_yml_path)
