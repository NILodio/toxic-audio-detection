# Toxic Audio Development Environment with Jupyter Notebook
# test
Welcome to the Toxic Audio project's development environment, designed to facilitate research and development processes.

## Getting Started

### Prerequisites

Make sure Docker is installed on your local machine before proceeding.

### Build Development Environment

```bash
make build_notebook
```

This command installs all the necessary dependencies, creating a Docker container with the Jupyter notebook running on port 8888.

### Start Development Environment

```bash
make start_notebook
```

Launch the development environment with this command. Jupyter notebook will be accessible at port 8888, enabling you to seamlessly begin your work on the Toxic Audio project.

Feel free to explore, experiment, and innovate within this dedicated development space. Happy coding!

### Update Development Environment

if you need to install a new package or library in the development environment, you can do so by modifying the `Dockerfile.anaconda` file and building the development environment again.

#### Example
```bash
RUN /opt/conda/bin/conda update -n base -c defaults conda && \
    /opt/conda/bin/conda install python=3.10 && \
    /opt/conda/bin/conda install anaconda-client && \
    /opt/conda/bin/conda install jupyter -y && \
    /opt/conda/bin/conda install librosa -y && \ # Add this line to install librosa
    /opt/conda/bin/conda install numpy pandas scikit-learn matplotlib seaborn pyyaml h5py keras -y && \
    /opt/conda/bin/conda upgrade dask
```
