# Prototyping: Quick reference

## Git

### Cloning the repository:

1. Go to the repository page on GitHub, and click on the green "Code" button.
2. Select "SSH" and copy the URL (for this repository, the URL is `git@github.com:prof-jose/PDAI25.git`).
3. Open a terminal and navigate to the folder where you want to clone the repository.
4. Run the following command:

```bash
git clone [URL]
```

### Updating the repository after each lecture

The following command fetches all new commits from the remote repository and merges them into the local repository:

```bash
git pull
```

## Virtual environment

A virtual environment is nothing more than a folder with a copy of the Python interpreter and the packages you install. 

This keeps the packages for a specific project separate from the system Python installation, preventing conflicts between different projects.

You can create a virtual environment using the Visual Studio Code interface or the terminal.

### Visual Studio Code

1. Open a python file. 
2. Click on the python version on the bottom left corner.
3. Select "Select Interpreter".
4. Click on "Create a new virtual environment".
5. If you have a "normal" python installation, select "venv". If you have installed Anaconda, select "conda". 
6. Select the Python version you want to use as the base interpreter.
7. Select the folder where you want to create the virtual environment. The current folder is a good choice.
8. Click on "Select Environment".


### Terminal (normal Python installation)

Creating an environment:

```bash
python3 -m venv [environment_name]
```

Activating the environment:
```bash
source venv/bin/activate
```

After activation, you can install and packages inside the environment with `pip` as usual:

```bash
pip install [package_name]
```

Deactivating the virtual environment:

```bash
deactivate
```

### Terminal (Anaconda installation)

Creating an environment:

```bash
conda create --name [environment_name]
```

Activating the environment:
```bash
conda activate [environment_name]
```

After activation, you can install and packages inside the environment with `conda` as usual:

```bash
conda install [package_name]
```

Deactivating the virtual environment:

```bash
conda deactivate
```

## Python tricks

### Context managers

In the Streamlit lecture, we saw the syntax

```python
with st.sidebar:
    # code here
```

You can learn the syntax as is, but if you want to understand what is happening behind the scenes:

- This use of `with` is called a context manager.

- In python, context managers are used to 
wrap a block of code
within an object
that runs extra predefined code before and after the given block of code.

- You might have often the following code to open a file:

```python
with open('file.txt', 'r') as f:
    print(f.read())
```
which is another common use of context managers. 

- You can check the Python documentation on context managers, including what they do and how to program your own ones here: http://book.pythontips.com/en/latest/context_managers.html



