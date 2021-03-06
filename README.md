# Overview of Deep Mimic Paper
[TOC]

## Introduction
This is the paper of SIGGRAPH 2018 paper:
"DeepMimic: Example-Guided Deep Reinforcement Learning of Physics-Based Character Skills".
The framework uses reinforcement learning to train a simulated humanoid to imitate a variety of motion skills from motion capture (mocap) data.

Original Project page of Authors: https://xbpeng.github.io/projects/DeepMimic/index.html



# Main Work of Mine Here

**Firstly**, The installation of `Linux Version` and some `problem solving`.

**Secondly**, Transfer bvh files of mocap to the format of deep mimic. [Not yet] Link: [bvh2mimic](https://github.com/zhaolongkzz/bvh2mimic)

**Thirdly**, **TODO**

## Installation
Here I provide how to use and make configuration of Deep Mimic in Ubuntu-16.04, and also offer some problem solving to code, from 0 to 7 and problem below, hope it can help you~     [[link](https://github.com/zhaolongkzz/DeepMimic_configuration/blob/master/README.md#0-dependencies)]

If you'd like to see the original version of installation by author 'Xuebin Peng', the [link here](https://github.com/zhaolongkzz/DeepMimic_configuration/blob/master/README_INSTALLATION.md).


### 0. Dependencies
C++:
- Bullet 2.87 (https://github.com/bulletphysics/bullet3/releases)
- Eigen (http://www.eigen.tuxfamily.org/index.php?title=Main_Page)
- OpenGL >= 3.2
- freeglut (http://freeglut.sourceforge.net/)
- glew (http://glew.sourceforge.net/)

Python:
- Python 3
- PyOpenGL (http://pyopengl.sourceforge.net/)
- Tensorflow (https://www.tensorflow.org/)
- MPI4Py (https://mpi4py.readthedocs.io/en/stable/install.html)

Misc:
- SWIG (http://www.swig.org/)
- MPI 
	- Windows: https://docs.microsoft.com/en-us/message-passing-interface/microsoft-mpi
	- Linux: `sudo apt install libopenmpi-dev`



### 1. Bullet2.88

[Bullet 2.88](https://github.com/bulletphysics/bullet3/releases)

Note that MPI must be installed before MPI4Py. When building Bullet, be sure to disable double precision with the build flag `DUSE_DOUBLE_PRECISION=OFF`.

```bash
./build_cmake_pybullet_double.sh -DUSE_DOUBLE_PRECISION=OFF
cd build_cmake
sudo make install
```

or you could install bullet by `sudo apt-get install libbullet-dev libbullet-extras-dev`, and see the [problem-2](https://github.com/zhaolongkzz/DeepMimic_configuration#2-bullet)

### 2. Eigen3

[Eigen](http://www.eigen.tuxfamily.org/index.php?title=Main_Page)

if your computer has one, can not be installed.
```bash
mkdir build_dir && cd build_dir
cmake ..
make install
```

`sudo apt-get install libeigen3-dev` is also a good way to install eigen3, set `MakeFile` see the [[problem_2](<https://github.com/zhaolongkzz/DeepMimic_configuration#2bullet>)] below.

### 3. OpenGL

```bash
sudo apt-get update
sudo apt-get install libglu1-mesa-dev freeglut3-dev mesa-common-dev
```

### 4. Freeglut

[Freeglut](http://freeglut.sourceforge.net/)

```bash
cmake .
make 
sudo make install
```

### 5. Glew

[Glew](http://glew.sourceforge.net/)

```bash
sudo apt-get install build-essential libxmu-dev libxi-dev libgl-dev
make
sudo make install
make clean
```

### 6. Env

[PyOpenGL](http://pyopengl.sourceforge.net/)

```bash
pip install PyOpenGL PyOpenGL_accelerate
pip install mpi4py
conda install numpy=1.15
conda install tensorflow-gpu=1.12
conda install PyOpenGL
```

### 7. Swig

[Swig](http://www.swig.org/)

If you are using anaconda and activate a environment, I suggest commenting out all the line of conda in `.bashrc`, and open a new terminal to install swig, because of the `libpcre.so.1` not find if it's in conda folder.

```bash
sudo apt-get install g++
sudo apt-get install libpcre3 libpcre3-dev
# download on previous link

tar -xzcf swig-xxxxx.tar.gz
cd swig-3.0.12
./configure

make 
sudo make install
```

not forget to add these two line in `.bashrc`

```bash
SWIG_PATH=/usr/local/share/swig/3.0.12
PATH=$PATH:$SWIG_PATH
```

MPI: `sudo apt install libopenmpi-dev`



## Problem

### 1. clang++ not found
make: clang++: Command not found
Makefile:49: recipe for target 'objs/Main.o' failed
make: *** [objs/Main.o] Error 127

`sudo apt-get install clang llvm`

use `clang --version` to see the version

### 2. bullet

in Ubuntu-16.04, you can install `bullet` by `sudo apt-get install libbullet-dev libbullet-extras-dev`

fix the location of the eigen and bullet, if you use the env in conda, like below:

```bash
EIGEN_DIR = /usr/include/eigen3
BULLET_INC_DIR = /usr/include/bullet

PYTHON_INC = /home/zzl/anaconda3/envs/mimic/include/python3.6m
PYTHON_LIB = /home/zzl/anaconda3/envs/mimic/lib/ -lpython3.6m
```

### 3. segmentation fault
```bash
Renderer: GeForce GTX 1060/PCIe/SSE2
OpenGL version supported 3.2.0 NVIDIA 384.130
Compiling shader: data/shaders/Mesh_VS.glsl
Compiling shader: data/shaders/VertColor_PS.glsl
Compiling shader: data/shaders/FullScreenQuad_VS.glsl
Compiling shader: data/shaders/DownSample_PS.glsl
Compiling shader: data/shaders/Mesh_VS.glsl
Compiling shader: data/shaders/DownSample_PS.glsl
Segmentation fault
```
when you encounter the problem of `Segmentation fault`.
there are two aspects:

- First remember to use NVIDIA <= 390, and (but now i use nvidia-415 is ok!)
- Second is to comment out #269 line in `DeepMimic.py`(#glutInitContextVersion(3, 2)). [issue#10](https://github.com/xbpeng/DeepMimic/issues/10)



### 4. when pelt boxes to robot
[issue#58](https://github.com/xbpeng/DeepMimic/issues/58)

when you use `x` to pelt the character with random boxes, then shows wrong message below: 
```bash
python: util/MathUtil.cpp:175: static tMatrix cMathUtil::RotateMat(const tVector &, double): Assertion `std::abs(axis.squaredNorm() - 1) < 0.0001' failed.
Aborted
```
try to adjust the equation `std::abs(axis.squaredNorm() - 1) < 0.1`, from 0.0001 to 0.1.



<br/>

<br/>

# Below is the original context of author

---

![Skills](images/teaser.png)

## Build
The simulated environments are written in C++, and the python wrapper is built using SWIG.
To install the python dependencies, run
```
pip install -r requirements.txt
```
Note that MPI must be installed before MPI4Py. When building Bullet, be sure to disable double precision with the build flag `USE_DOUBLE_PRECISION=OFF`.

### Windows
The wrapper is built using `DeepMimicCore.sln`.

1. Select the `x64` configuration from the configuration manager.

2. Under the project properties for `DeepMimicCore` modify `Additional Include Directories` to specify
	- Bullet source directory
	- Eigen include directory
	- python include directory

3. Modify `Additional Library Directories` to specify
	- Bullet lib directory
	- python lib directory

4. Build `DeepMimicCore` project with the `Release_Swig` configuration and this should
generate `DeepMimicCore.py` in `DeepMimicCore/`.


### Linux
1. Modify the `Makefile` in `DeepMimicCore/` by specifying the following,
	- `EIGEN_DIR`: Eigen include directory
	- `BULLET_INC_DIR`: Bullet source directory
	- `PYTHON_INC`: python include directory
	- `PYTHON_LIB`: python lib directory

2. Build wrapper,
	```
	make python
	```
This should generate `DeepMimicCore.py` in `DeepMimicCore/`


## How to Use
Once the python wrapper has been built, training is done entirely in python using Tensorflow.
`DeepMimic.py` runs the visualizer used to view the simulation. Training is done with `mpi_run.py`, 
which uses MPI to parallelize training across multiple processes.

`DeepMimic.py` is run by specifying an argument file that provides the configurations for a scene.
For example,
```
python DeepMimic.py --arg_file args/run_humanoid3d_spinkick_args.txt
```

will run a pre-trained policy for a spinkick. Similarly,
```
python DeepMimic.py --arg_file args/kin_char_args.txt
```

will load and play a mocap clip.


To train a policy, run `mpi_run.py` by specifying an argument file and the number of worker processes.
For example,
```
python mpi_run.py --arg_file args/train_humanoid3d_spinkick_args.txt --num_workers 4
```

will train a policy to perform a spinkick using 4 workers. As training progresses, it will regularly
print out statistics and log them to `output/` along with a `.ckpt` of the latest policy.
It typically takes about 60 millions samples to train one policy, which can take a day
when training with 16 workers. 16 workers is likely the max number of workers that the
framework can support, and it can get overwhelmed if too many workers are used.

A number of argument files are already provided in `args/` for the different skills. 
`train_[something]_args.txt` files are setup for `mpi_run.py` to train a policy, and 
`run_[something]_args.txt` files are setup for `DeepMimic.py` to run one of the pretrained policies.
To run your own policies, take one of the `run_[something]_args.txt` files and specify
the policy you want to run with `--model_file`. Make sure that the reference motion `--motion_file`
corresponds to the motion that your policy was trained for, otherwise the policy will not run properly.


## Interface
- the plot on the top-right shows the predictions of the value function
- right click and drag will pan the camera
- left click and drag will apply a force on the character at a particular location
- scrollwheel will zoom in/out
- pressing 'r' will reset the episode
- pressing 'l' will reload the argument file and rebuild everything
- pressing 'x' will pelt the character with random boxes
- pressing space will pause/resume the simulation
- pressing '>' will step the simulation one step at a time


## Mocap Data
Mocap clips are located in `data/motions/`. To play a clip, first modify 
`args/kin_char_args.txt` and specify the file to play with
`--motion_file`, then run
```
python DeepMimic.py --arg_file args/kin_char_args.txt
```

The motion files follow the JSON format. The `"Loop"` field specifies whether or not the motion is cyclic.
`"wrap"` specifies a cyclic motion that will wrap back to the start at the end, while `"none"` specifies an
acyclic motion that will stop once it reaches the end of the motion. Each vector in the `"Frames"` list
specifies a keyframe in the motion. Each frame has the following format:
```
[
	duration of frame in seconds (1D),
	root position (3D),
	root rotation (4D),
	chest rotation (4D),
	neck rotation (4D),
	right hip rotation (4D),
	right knee rotation (1D),
	right ankle rotation (4D),
	right shoulder rotation (4D),
	right elbow rotation (1D),
	left hip rotation (4D),
	left knee rotation (1D),
	left ankle rotation (4D),
	left shoulder rotation (4D),
	left elbow rotation (1D)
]
```

Positions are specified in meters, 3D rotations for spherical joints are specified as quaternions `(w, x, y ,z)`,
and 1D rotations for revolute joints (e.g. knees and elbows) are represented with a scalar rotation in radians. The root
positions and rotations are in world coordinates, but all other joint rotations are in the joint's local coordinates.
To use your own motion clip, convert it to a similar style JSON file.
