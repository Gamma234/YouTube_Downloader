## YouTube_Downloader_v4

----

### \[Contents]

+ YouTube_Downloader_v4
  + data
    + tool
      + YouTube_DLer_v4.py
    + save_path.txt
  + ip_file.txt
  + YouTube_Downloader_v4.py
  
----

### \[Required Packages]

pytube, ffmpeg, re, os, shutil

----

### \[Run Codes in an IDE]

1. Complete the following for "IDE".  
   (1) Install packages.     
   ```
       pip install pytube  
       pip install pytube3  
       pip install ffmpeg-python  
   ```    

2. Complete the following for "Windows 10".  
   (1) Download "ffmpeg" from website (https://github.com/BtbN/FFmpeg-Builds/releases).  
   (2) You must check whether it contains the "bin" folder or not.  
   (3) Change the file name to "ffmpeg" and put in "C:\".  
   (4) Add "C:\ffmpeg\bin" in "Environment Variable" -> "System Variables" -> "Path".  
   (5) Go to CMD and type "ffmpeg" as a command to check whether it is successful or not.  
 
3. Run "YouTube_Downloader_v4.py" in an IDE.

----

### \[Run Codes in the CMD in Windows 10]

1. Complete the following for "Windows 10".  
   (1) Download and install "python" from website (https://www.python.org/).  
   (2) Go to CMD and type some commands to install packages.  
   ```
       pip install pytube  
       pip install pytube3  
       pip install ffmpeg-python  
   ```   
   (3) Download "ffmpeg" from website (https://github.com/BtbN/FFmpeg-Builds/releases).  
   (4) You must check whether it contains the "bin" folder or not.  
   (5) Change the file name to "ffmpeg" and put in "C:\".  
   (6) Add "C:\ffmpeg\bin" in "Environment Variable" -> "System Variables" -> "Path".  
   (7) Go to CMD and type "ffmpeg" as a command to check whether it is successful or not.  

2. Type "python YouTube_Downloader_v4.py" as a command to run codes in the CMD.

----

### \[Error Solution]

Problem | Solution
------- | --------
cipher  | Modify "pytube/extract.py". Change "cipher" at the line 301 to "signatureCipher".  

----

### \[References]

+ python
  + https://www.python.org/
+ pytube — pytube 10.4.1 documentation
  + https://python-pytube.readthedocs.io/en/latest/
+ ffmpeg
  + https://ffmpeg.org/
+ FFmpeg-Builds
  + https://github.com/BtbN/FFmpeg-Builds/releases

