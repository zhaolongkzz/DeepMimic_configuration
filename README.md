# Overview of Deep Mimic Paper

[TOC]

## Introducation
Code accompanying the SIGGRAPH 2018 paper:
"DeepMimic: Example-Guided Deep Reinforcement Learning of Physics-Based Character Skills".
The framework uses reinforcement learning to train a simulated humanoid to imitate a variety
of motion skills from mocap data.

Project page: https://xbpeng.github.io/projects/DeepMimic/index.html


Maybe this one also helps you, [link](https://github.com/bsivanantham/DeepMimic/blob/master/README.Install.md).


![Skills](images/teaser.png)

### Dependencies
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


## Installation 
Here provided how to use and make configuration of Deep Mimic in Ubuntu-16.04

If you'd like to see the original version of installation by authors 'Xuebin Peng', the [link here](https://github.com/xbpeng/DeepMimic).


### 1.Bullet2.88

[Bullet 2.88](https://github.com/bulletphysics/bullet3/releases)

```bash
./build_cmake_pybullet_double.sh
cd build_cmake
sudo make install
```

### 2.Eigen3

[Eigen](http://www.eigen.tuxfamily.org/index.php?title=Main_Page)

if your computer has one, can not be installed.
```bash
mkdir build_dir && cd build_dir
cmake ..
make install
```

### 3.OpenGL

```bash
sudo apt-get update
sudo apt-get install libglu1-mesa-dev freeglut3-dev mesa-common-dev
```

### 4.Freeglut

[Freeglut](http://freeglut.sourceforge.net/)

```bash
cmake .
make 
sudo make install
```

### 5.Glew

[Glew](http://glew.sourceforge.net/)

```bash
sudo apt-get install build-essential libxmu-dev libxi-dev libgl-dev
make
sudo make install
make clean
```

### 6.env

[PyOpenGL](http://pyopengl.sourceforge.net/)


```bash
pip install PyOpenGL PyOpenGL_accelerate
pip install mpi4py
conda install numpy=1.15
conda install tensorflow-gpu=1.12
conda install PyOpenGL
```

### 7.Swig

[Swig](http://www.swig.org/)

If you are using anaconda and activate a environment, I suggest commenting out all the line of conda in `.bashrc`, and open a new terminal to install swig, because of the `libpcre.so.1` not find if it's in conda floder.

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

### 1.clang++ not found
make: clang++: Command not found
Makefile:49: recipe for target 'objs/Main.o' failed
make: *** [objs/Main.o] Error 127

`sudo apt-get install clang llvm`

use `clang --version` to see the version

### 2.Bullet

in Ubuntu-16.04, you can install `bullet` by `sudo apt-get install libbullet-dev libbullet-extras-dev`


fix the location of the eigen and bullet, if you use the env in conda, like below:

```bash
EIGEN_DIR = /usr/include/eigen3
BULLET_INC_DIR = /usr/include/bullet

PYTHON_INC = /home/zzl/anaconda3/envs/mimic/include/python3.6m
PYTHON_LIB = /home/zzl/anaconda3/envs/mimic/lib/ -lpython3.6m
```

### 3.Segmentation fault
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
when you encounter the problem of `Segmentation fault`, there are two aspects, first remember to use NVIDIA <= 390, and second is to comment out #269 line (#glutInitContextVersion(3, 2))







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
