# Project Unnamed
The project is yet to be named. But, it's an hybrid summarization tool, which uses both traditional mathematical algorithms as well as modern AI-based methods to summarize research articles.
## Install llama-cpp-python for GPU as follows:
```
sudo apt install cmake
sudo apt install gcc-11 g++-11
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 60 --slave /usr/bin/g++ g++ /usr/bin/g++-11
gcc --version
g++ --version
CMAKE_ARGS="-DGGML_CUDA=on" FORCE_CMAKE=1 pip install llama-cpp-python --force-reinstall --no-cache-dir
```
