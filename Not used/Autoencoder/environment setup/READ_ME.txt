You don't need to install python 3.8 or any of the libraries on your machine.
We're gonna create a custom envirment with those, so it won't interfere with your system/default setup.


Run NVidia cuda network installer (cuda_10.1.243_win10_network)
- Use custom installation options.
- Only download CUDA.
- Driver and other components will downgrade your NVidia setup and are not needed anyway.


Inside cudnn-10.1-windows10-x64-v7.6.4.38.zip is the cuda folder.
Copy the three folders from that folder into:
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1


Set the folders paths:
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\bin
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.1\libnvvp
into your environment variable path.
- You might need to set it for the path in both system and user variables.


Run Miniconda3 installer.
- Install for all users.
- Remove second check to register Miniconda3 as system standard.
- This is your custom environment and is REQUIRED for cuda to work! It won't work in the standard CMD.


Restart you computer, as the enviroment variable and NVidia libraries needs to be loaded properly


Open miniconda3 by searching it in the windows menu.
Create a custom enviroment by typing the command:
conda create --name tf_2.3.1 python==3.8
- tf_2.3.1 is the name.
- If it asks to install something, just hit yes.
Open the custom enviroment by typing the command:
conda activate tf_2.3.1


We now need to download the libraries.
You can do this by hand, or running the file:
install_libraries.txt
Just open the location in the environment and run the command:
cmd < install_libraries.txt