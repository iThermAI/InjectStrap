# InjectStrap
![Travis (.com)](https://img.shields.io/travis/com/ithermai/InjectStrap)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/ithermai/InjectStrap) 
![Lines of code](https://img.shields.io/tokei/lines/github/ithermai/InjectStrap)
![GitHub repo size](https://img.shields.io/github/repo-size/ithermai/InjectStrap)
![GitHub last commit](https://img.shields.io/github/last-commit/ithermai/InjectStrap)

This repository is designed for extracting features from videos as part of the Smart4ALL experiment. The experiment involves using thermal videos to extract thermal properties and generation cycles of [components](https://elvez.si/METALLISED-COMPONENTS/) from the [Elvez compnay](https://elvez.si/). The videos were recorded using a PI thermal camera. This repository can work real-time alongside a camera. 

In the video that follows, a component can be observed as it moves in front of the camera. By studying videos like this one, we can record the thermal properties of the component as it appears in front of the camera in tabular form. The brought videos is just a sample. 



https://user-images.githubusercontent.com/69720514/215268755-2370a91e-c771-4657-84fe-a44cbfe04a8f.mp4

After identifying a static frame that encompasses all parts of the component, we gather information from 11 distinct regions of the component. These regions are illustrated in the image below.

![image](https://user-images.githubusercontent.com/69720514/215269316-5e85b14d-95d6-407d-8e7d-6126b74ae18b.jpg)

## How to run the program
Running this program is straightforward. To generate a dataset from the videos, the main.py script must be executed. This script accepts two arguments: `vid_dir` which is the directory containing the input videos, and `save_dir` which is the directory and name of the generated dataset. By executing the following code lines, the script will run and the generated dataset will be saved in the specified directory and filename.

```shell
 python main.py --vid_dir "./vid.ravi" --save_dir "./result/dataset-vid1.csv"
```
or
```shell
 python3 main.py --vid_dir "./vid.ravi" --save_dir "./result/dataset-vid1.csv"
```

## Requirements
```shell
  python>=3.8
  numpy>=1.23
  pandas>=1.3
  opencv-python>=4.6
```

### Acknowledgements
This project was supported by the Smart4ALL project in Horizon 2020. 
