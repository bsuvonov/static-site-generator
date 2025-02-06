# Static Site Generator

This tool allows you to easily convert your Markdown documents into HTML files, ideal for blogging and creating websites with minimal effort.

## Features

- **Markdown to HTML Conversion**: Write your blog posts or documents in Markdown and convert them to HTML automatically.
- **Custom CSS Support**: Apply your own custom stylesheets to the generated HTML files for a personalized look.
- **Static File Support**: Include images and other necessary files for your site by placing them in the `static` folder, which will be copied over to the `public` folder.

## Project Structure
- **src/**: Contains source code
- **content/**: This folder should contain all of your Markdown files. Each file will be converted to an HTML page.
- **static/**: Place your images, CSS files, and other static assets here. These files will be included in the generated output folder.

## How to Use

1. **Clone the repository**:
   ```bash
   git https://github.com/bsuvonov/static-site-generator.git
   cd static-site-generator
   ```
2. **Place your files**
   - Place your md files in `content` folder
   - Place your styles.css and any other assets in `static` folder (optional)
3. **Run the program**
   ```bash
   ./main.sh
   ```   

## Contribute
If you found any bug, implemented a new feature or would like to request a new feature, feel free to open a pull request or issue in this repo.
