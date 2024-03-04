import re

from src.backend.shared_functions import *

pornhub_pattern = re.compile(r'(.*?)pornhub.com(.*)')
hqporner_pattern = re.compile(r'(.*?)hqporner.com(.*)')
xnxx_pattern = re.compile(r'(.*?)xnxx.com(.*)')
xvideos_pattern = re.compile(r'(.*?)xvideos.com(.*)')
eporner_pattern = re.compile(r'(.*?)eporner.com(.*)')


class CLI():
    def __init__(self):
        while True:
            setup_config_file()
            self.conf = ConfigParser()
            self.conf.read("config.ini")
            self.menu()


    def license(self):
        if not self.conf["License"]["accepted"] == "true":
            license = input(f"""
GPL License Agreement for Porn Fetch
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
NO LIABILITY FOR END USER USE
Under no circumstances and under no legal theory, whether in tort, contract, or otherwise, shall the copyright holder or contributors be liable to You for any direct, indirect, special, incidental, consequential or exemplary damages of any character including, without limitation, damages for loss of goodwill, work stoppage, computer failure or malfunction, loss of data or any and all other commercial damages or losses, even if such party shall have been informed of the possibility of such damages.
This limitation of liability shall not apply to liability for death or personal injury resulting from such party’s negligence to the extent applicable law prohibits such limitation. Some jurisdictions do not allow the exclusion or limitation of incidental or consequential damages, so this exclusion and limitation may not apply to You.
This Agreement represents the complete agreement concerning the subject matter hereof.

Disclaimer:
Porn Fetch is NOT associated with any of the websites. Using this tool is against the ToS of every website. Usage of Porn Fetch is at your own risk. I (the developer) am not liable for any of your actions. This tool is not meant to be used for mass downloading content from websites or downloading copyright protected material.


Do you accept the license?  [yes,no]
---------------------------------->:""")

            if license == "yes":
                self.conf = "your_mom"






    def menu(self):
        options = input(f"""
1) Download a Video
2) Get videos from a model
3) Get videos from a PornHub playlist
4) Search for videos
5) Search a file for URLs and Model URLs
6) Settings

98) Credits
99) Exit

------------------>:""")


        if options == "1":
            self.process_video()



    def load_user_settings(self):





    def save_user_settings(self):






    def process_video(self, url=None):
        if url is None:
            url = input(f"Please enter the Video URL -->:")


        video = check_video(url=url, language=self.)








    def process_model(self):



    def






