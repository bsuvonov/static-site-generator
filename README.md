# Static Site Generator

![demo](https://raw.githubusercontent.com/wiki/bsuvonov/static-site-generator/images/demo.png)

This tool allows to easily convert Markdown documents into HTML files, ideal for blogging and creating websites with minimal effort.

## Features

- **Markdown to HTML Conversion**: Converts Markdown documents to HTML automatically.
- **Custom CSS Support**: Supports custom stylesheets to be applied to the generated HTML files for a personalized look.
- **Static File Support**: Keeps the original linkage between static files and markdown files in the output html files in tact!

## How to Use

1. **Clone the repository**:
   
   ```bash
   git clone https://github.com/bsuvonov/static-site-generator.git
   cd static-site-generator
   ```
   
3. **Place your files**
   
   - Place md files in `content` folder. Each file will be converted to an HTML page.
   - Place styles.css and any other assets in `static` folder (optional). These files will be included in the generated output folder.
     
5. **Run the program**

   ```bash
   ./main.sh
   ```   

## Contribute
If you found any bug, implemented a new feature or would like to request a new feature, feel free to open a pull request or issue in this repo.
