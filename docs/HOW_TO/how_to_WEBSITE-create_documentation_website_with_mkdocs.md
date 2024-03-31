# Create Documentation Website with MkDocs

This guide will show you how to create a develop environment for a documentation website using MkDocs.

## Problem

You want to create a documentation website with MkDocs for documenting projects, APIs, or any other content.

## Background

MkDocs generates websites from markdown files and can be accessed locally for rapid development and deployed to a web server (ex: GitHub Pages). It prevents the need to write HTML, CSS, and JS, and let developer focuses on only the documentation.

## Solution

### Step 1. Setup MkDocs

1. Install Python and pip.
    1. In Windows, download Python from [Python official website](https://www.python.org/downloads/).
    2. In Linux, use corresponding package manager to install Python. Following is an example for Debian-based systems.
        ```bash
        sudo apt install python3 python3-pip
        ```
2. (optional, recommended) Create and activate a virtual environment.
    1. In Windows, open Command Prompt, PowerShell, or [PowerShell 7](https://github.com/PowerShell/PowerShell/releases) and run the following command. You need to replace `Python312` with your installed version, and `cd` into your project directory before execution.
        ```pwsh
        C:\Python312\python.exe -m venv venv
        .\venv\Scripts\activate
        ```
    2. In Linux, open Terminal and run the following command. You need to replace `python3.12` with your installed version, and `cd` into your project directory before execution.
        ```bash
        python3.12 -m venv venv
        source venv/bin/activate
        ```
3. Install MkDocs.
    ```bash
    pip install mkdocs mkdocs-material
    ```
4. (optional) Install MkDocs plugins like [mkdocs-nav-weight](https://github.com/shu307/mkdocs-nav-weight)
    ```bash
    pip install mkdocs-nav-weight
    ```
5. Initialize MkDocs project.
    ```bash
    mkdocs new .
    ```
6. Serve website locally for development. You can access the website at `127.0.0.1:8000` with default settings in your browser.
    ```bash
    mkdocs serve
    ```
7. After development, deploy your website to a web server.

After project initialized, you can edit `mkdocs.yml` for configuration, and edit markdown files in `docs` directory for content. Markdown files will be pages, directory with `index.md` can hold subpages.

### Step 2. Development Routine

1. Serve website locally. You need to `cd` into your project directory before execution.
    ```bash
    mkdocs serve
    ```
2. Edit markdown files in `docs` directory. MkDocs will automatically reload the website when files are modified.

## Reference

1. [https://www.mkdocs.org/](https://www.mkdocs.org/)
2. [https://squidfunk.github.io/mkdocs-material/](https://squidfunk.github.io/mkdocs-material/)
3. [YouTube - James Willett - How to Create STUNNING Code Documentation With MkDocs Material Theme](https://youtu.be/Q-YA_dA8C20?si=2t6VQOF58xb62juB)
