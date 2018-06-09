# Computer vision fish frame proposal

This notebook shows how you can benefit from [Microsoft Computer vision](https://azure.microsoft.com/en-au/services/cognitive-services/computer-vision/) to analyse video frames. This sample analyses the underwater video and extracts frames and retruns back frames that has fish in it. Depends on your use case, you can adjust the extract rate. You can define to extract a frame every 20 seconds.

Please note in your production environment we won't recommend adding videos and extracted frames into your source repository. It's only added as a sample and for your reference only.


[Steve Van Bodegraven](https://www.linkedin.com/in/svanbodegraven/), works directly with fisheries across Australia and lead projects that help fisheries to adopt new technologies and improve the manual processes by using AI and machine learning. He came up with `frame proposal` term. 


Imagine you are a marine biologist! On weekly basis, you go to specific spots in the ocean to study fish diversity, abundance and behaviour of species over time. You will use Baited remote underwater video, named BRUV to record what’s happening underwater. This part of the job if you like water and outdoor actives are super awesome!
Then you will come back from the work excursion and classify recorded videos based on date, time and location of the recording. After that, you will start watching recordings. If you think all the video recordings will like planet earth or other underwater documentaries, YOU ARE WRONG!
Most of the recording will be the body of water and empty of life for minutes then there will be a magical moment that you will see one or two fishes, sharks or school of fish then again the body of water.
Imagine you task is watching videos frame by frame and write done on which frame you saw fish or any activates. This process is labour intensive and it’s not fun!

![alt text](https://4.bp.blogspot.com/-pKPpAnFeWHs/WxudTPz82vI/AAAAAAAACVI/wW69O_97VOMQVBqd7V62qnZUn3B7KElqgCLcBGAs/s640/cycle.PNG "Your life as marine biologist")


As a scientist, you will like to maximize your fun and minimize the boring parts. You want to do more recording and then analyzing fish frames and avoid watching the whole videos!

The question is, how we can automate the process? What we want is replace the computer with a human to see the videos and tells us which frame has fish in it.  In the engineering world, this type of tasks called computer vision. We want computer sees the photos or videos and analyses them and have the same understanding as human.

The easiest approach is using out of the box services to analyse the image and get information about visual content found in it. I used Microsoft computer vision API which can recognise 2000 objects to find out if there is a fish in the image or not. 

![alt text](https://1.bp.blogspot.com/-NHcdt-21bew/WxugM_DR90I/AAAAAAAACVU/HbyqCZvzKDY0Kux1rvlv_Vc1soCRyS5PwCLcBGAs/s640/Steps.PNG "How it works")

First, you need to get subscription key to use Microsoft computer vision, you can get free keys from [here] (https://azure.microsoft.com/en-us/try/cognitive-services/)  I used the paid API to avoid hitting the limits on calling API per minute.

![alt text](https://3.bp.blogspot.com/-PEdBPfGdTYo/WxunKlutulI/AAAAAAAACVg/DwvKpY-KvkM9dSe33TYv1LXKfaWanj-uACLcBGAs/s400/pricing.PNG "pricing")

The notebook is self-explanatory, It's written in python 3.5 and you can easily run it after cloning the repository.  If you don't have anaconda, you can download it from [here] (https://anaconda.org/download)


[read it on my blog](http://azadehkhojandi.blogspot.com/2018/06/computer-vision-fish-frame-proposal.html)

![alt text](https://4.bp.blogspot.com/-_u66jCsdYoY/WxuqDr---jI/AAAAAAAACVs/8tDQki5BH506vbfCG9qL_8LKBvS4m6T7wCLcBGAs/s640/anaconda.PNG "command prompt")

![alt text](https://3.bp.blogspot.com/-StxaMePPswk/Wxuq4F3gNcI/AAAAAAAACV0/HzzvCyHET-Y69s76QQx8osAlwLibfSllQCLcBGAs/s640/notebookhomepage.PNG "notebook home page")

All you need to do is copy your video into the videos folder. Then open "Export_Frames_From_Video.ipynb"
Now you need to update the computer vision subscription key and replace it with your key

![alt text](https://4.bp.blogspot.com/-z0NhakHb5vM/WxurYqkBT7I/AAAAAAAACV8/fNfN0ip8XF0XhwEjjcWVJ51wpPgErr-VgCLcBGAs/s640/subscriptionKey.PNG "subscriptionKey")

Run each block from the beginning. Select the first block and then click on "Run" from the toolbar and continue till after Analysing the extracted frames. extract frames from video block, extracts a frame every 2 seconds, based on your experience you can increase or decrease the export rate.
Then Alanlysing the extracted frames, analyses every extracted frame and shows the frames that it detected fish in it. It also show it's confidence level.

![alt text](https://1.bp.blogspot.com/-yzyQ0qTcwBI/WxuszErviKI/AAAAAAAACWQ/8VxieoVFZDsRjBrcVKYa80UKF88YgzqMwCLcBGAs/s640/analyse.PNG "anlysing the images")

In the end, you will get two CSV file. The first file lists all the frames and the second one has a list of frames which computer detected fish in it.

If you want to investigate more or add more frames to the extracted frames, you can update the parameters and continue running the blocks if it's required.
