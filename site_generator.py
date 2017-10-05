from os import path, makedirs
import json
from collections import defaultdict
from argparse import ArgumentParser

import markdown
from livereload import Server
from jinja2 import Environment, FileSystemLoader


def make_cmd_arguments_parser():
    parser_description = 'The script generates the documentation from .md files with structure describe in config.json file.'
    parser = ArgumentParser(description=parser_description)
    parser.add_argument('-l', '--livereload',
                        help='Run in livereload mode',
                        action='store_true')
    parser.add_argument('-b', '--build',
                        help='Build or rebuild your encyclopedia from source files...',
                        action='store_true')
    return parser


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


def render_html_from_template(template_basename, **template_arguments):
    root_folder = '/19_site_generator/'
    template_directory = 'templates'
    static_folder_path = '{root_folder}static_files/'.format(root_folder=root_folder)

    jinja_environment = Environment(loader=FileSystemLoader(template_directory),
                                    trim_blocks=True,
                                    lstrip_blocks=True)
    template = jinja_environment.get_template(template_basename,
                                              globals={'static': static_folder_path,
                                                       'root': root_folder}
                                              )
    return template.render(**template_arguments)


def generate_html_from_markdown_file(markdown_file_path):
    markdown_data = fetch_encode_data_from_file(markdown_file_path)
    return markdown.markdown(markdown_data)


def group_by_topic_articles_dict(config_data, articles_name='articles', topic_name='topic'):
    group_by_topic_articles_dict = defaultdict(list)
    for article_info in config_data[articles_name]:
        article_topic = article_info.get(topic_name)
        group_by_topic_articles_dict[article_topic].append(article_info)
    return group_by_topic_articles_dict


def save_render_html_from_template(template_basename, output_html_file_path, **template_arguments):
    rendered_html = render_html_from_template(template_basename=template_basename,
                                              **template_arguments)
    save_data_to_file(user_data=rendered_html,
                      output_file_path=output_html_file_path)


def save_table_of_contents_html_file(config_data, result_file_path):
    articles_info = group_by_topic_articles_dict(config_data)
    topics_info = {config['slug']: config['title'] for config in config_data['topics']}
    save_render_html_from_template(
        template_basename='index.html',
        output_html_file_path=result_file_path,
        articles_info=articles_info,
        topics_info=topics_info
    )


def save_articles_html_files_from_markdown(config_data, result_folder):
    articles_storage_path = 'articles'
    for article_params in config_data['articles']:
        article_path_in_storage = article_params['source']
        transformed_markdown = generate_html_from_markdown_file(
            path.join(articles_storage_path, article_path_in_storage)
        )
        save_render_html_from_template(
            template_basename='article.html',
            output_html_file_path=path.join(result_folder, article_path_in_storage.replace('.md', '.html')),
            article_params=article_params,
            article_content=transformed_markdown
        )


def make_site():
    try:
        config_articles_file_path = 'config.json'
        config_data = json.loads(fetch_encode_data_from_file(config_articles_file_path))
        result_articles_folder = path.join('static_files', 'articles')
        save_table_of_contents_html_file(config_data=config_data, result_file_path='index.html')
        save_articles_html_files_from_markdown(config_data=config_data, result_folder=result_articles_folder)
    except (ValueError, FileExistsError) as error:
        print('Error: ', error)


if __name__ == '__main__':
    cmd_args_parser = make_cmd_arguments_parser()
    cmd_args = cmd_args_parser.parse_args()
    if not any([cmd_args.livereload, cmd_args.build]):
        cmd_args_parser.error("One of --livereload or --build must be given. Type -h to help.")
    if cmd_args.build:
        print('Build encyclopedia from source files...\n')
        make_site()
    if cmd_args.livereload:
        print('Start watch files...\n')
        server = Server()
        server.watch('templates/*.html', make_site)
        server.watch('articles/**/*.md', make_site)
        server.serve(root='')
