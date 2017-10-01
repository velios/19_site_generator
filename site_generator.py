from os import path, makedirs
import json
from collections import defaultdict

import markdown
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape


def save_data_to_file(user_data, output_file_path):
    if not user_data:
        raise ValueError('Can\'t save data to file: ', 'empty data')
    if path.dirname(output_file_path):
        makedirs(path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, mode='w', encoding='utf-8') as file_handler:
        file_handler.write(user_data)


def fetch_encode_data_from_file(file_path, encoding='utf-8'):
    if not path.exists(file_path):
        raise FileExistsError('File doesn\'t exist: ', file_path)
    with open(file_path, encoding=encoding) as file_handler:
        file_data = file_handler.read()
        return file_data


def render_html_from_template(template_full_path, **kwargs):
    template_directory, template_file_name = path.split(template_full_path)
    jinja_environment = Environment(loader=FileSystemLoader(template_directory),
                                    trim_blocks=True,
                                    lstrip_blocks=True,)
    template = jinja_environment.get_template(template_file_name)
    return template.render(**kwargs)


def generate_html_from_markdown_file(markdown_file_path):
    markdown_data = fetch_encode_data_from_file(markdown_file_path)
    return markdown.markdown(markdown_data)

# Unpure funcitions
def group_by_topic_articles_dict(config_data, articles_name='articles', topic_name='topic'):
    group_by_topic_articles_dict = defaultdict(list)
    for article_info in config_data[articles_name]:
        article_topic = article_info.get(topic_name)
        group_by_topic_articles_dict[article_topic].append(article_info)
    return group_by_topic_articles_dict


def generate_table_of_contents_html_file(config_data, result_folder):
    articles_info = group_by_topic_articles_dict(config_data)
    topics_info = {config['slug']: config['title'] for config in config_data['topics']}

    html = render_html_from_template(template_full_path=path.join('templates', 'index.html'),
                                     articles_info=articles_info,
                                     topics_info=topics_info,)
    save_data_to_file(html, 'index.html')


def generate_articles_html_files_from_markdown(config_data, result_folder):
    articles_storage_path = 'articles'
    for article_params in config_data['articles']:
        article_path_in_storage = article_params['source']
        transformed_markdown = generate_html_from_markdown_file(
            path.join(articles_storage_path, article_path_in_storage)
        )
        article_html = render_html_from_template(
            template_full_path=path.join('templates', 'article.html'),
            article_params=article_params,
            article_content=transformed_markdown
        )
        save_data_to_file(article_html, path.join(result_folder, article_path_in_storage.replace('.md', '.html')))


def make_site():
    try:
        config_articles_file_path = 'config.json'
        config_data = json.loads(fetch_encode_data_from_file(config_articles_file_path))
        result_folder = 'site'
        generate_table_of_contents_html_file(config_data=config_data, result_folder=result_folder)
        generate_articles_html_files_from_markdown(config_data=config_data, result_folder=result_folder)
    except (ValueError, FileExistsError) as error:
        print('Error: ', error)


if __name__ == '__main__':
    make_site()
    server = Server()
    server.watch('templates/*.html', make_site)
    server.watch('articles/**/*.md', make_site)
    server.serve(root='')
