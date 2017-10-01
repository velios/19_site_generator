# Encyclopedia

The script generates the documentation from markdown files with structure describe in `config.json` file.

### Where see result
Visit https://velios.github.io/19_site_generator/

### How to install

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
# Download repository from GitHub
$ git clone https://github.com/velios/19_site_generator.git
# Change folder to download folder
$ change to clone directory
# install requirements
$ pip install -r requirements.txt # alternatively try pip3
```

### Structure
* `articles/` - folder with original articles writen with [markdown syntax](https://ru.wikipedia.org/wiki/Markdown)
* `site/` - folder with files for publication
* `templates/` - folder with templates in [Jinja2 format](http://jinja.pocoo.org/docs/2.9/templates/#template-inheritance)
* `config.json` - file describing the structure table of contents, titles, topics and path to source files
* `site_generator.py` - script to make it all work together

### How to use
##### Add new articles
You can write articles with [markdown syntax](https://ru.wikipedia.org/wiki/Markdown) and add it to `articles` folder. After that, you need to describe new file in `config.json`.

##### Build encyclopedia from source
```bash
$ python site_generator.py --build # alternatively try python3
```

##### Make markup with realtime watch changes with livereload
```bash
$ python site_generator.py --livereload # alternatively try python3
```

### Site is tested on W3C Markup Validation Service

To check this follow the [W3C Markup Validation Service link](https://validator.w3.org/nu/?doc=https%3A%2F%2Fvelios.github.io%2F19_site_generator%2F)




# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
