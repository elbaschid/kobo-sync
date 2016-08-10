import os
import re
import json

import click
import peewee
import requests

from peewee import Model
from collections import defaultdict
from playhouse.sqlite_ext import SqliteExtDatabase


GITHUB_GISTS_API = 'https://api.github.com/gists'
GOOGLE_BOOKS_API = 'https://www.googleapis.com/books/v1/volumes'


db_proxy = peewee.Proxy()


class Content(Model):
    id = peewee.TextField(primary_key=True, db_column='ContentID')

    book_title = peewee.TextField(db_column='BookTitle')
    title = peewee.TextField(db_column='Title')
    isbn = peewee.TextField(db_column='ISBN')

    def __str__(self):
        return self.book_title or self.title or ''

    class Meta:
        database = db_proxy
        db_table = 'content'


class Bookmark(Model):
    id = peewee.TextField(primary_key=True, db_column='BookmarkID')

    content_id = peewee.TextField(db_column='ContentID')

    text = peewee.TextField(db_column='Text')
    annotation = peewee.TextField(db_column='Annotation')

    def get_content(self):
        content_id, *__ = self.content_id.split('!', 1)
        return Content.get(Content.id == content_id)

    @classmethod
    def select_with_title(cls):
        for bookmark in Bookmark.select().distinct():

            if str(bookmark).strip():
                yield bookmark

    def __str__(self):
        content = self.text or self.annotation or ''
        content, __ = re.subn(r'\s+', ' ', content)
        return content.strip()

    class Meta:
        database = db_proxy
        db_table = 'Bookmark'


@click.command()
@click.option('--github-token', default='', envvar='GITHUB_API_TOKEN')
@click.option('--gist')
@click.option('--db-file',
              default='/Volumes/KOBOeReader/.kobo/KoboReader.sqlite')
def main(github_token, gist, db_file):
    db_proxy.initialize(SqliteExtDatabase(db_file))

    grouped_annotations = defaultdict(list)

    for bookmark in Bookmark.select_with_title():
        content = bookmark.get_content()
        grouped_annotations[content.isbn].append(bookmark)

    files = {}

    for isbn, annotations in grouped_annotations.items():
        content = Content.get(Content.isbn == isbn)

        file_content = []
        file_content.append('# Title: {}'.format(content.title))
        file_content.append('')

        if isbn:
            response = requests.get(GOOGLE_BOOKS_API,
                                    params={'q': 'ISBN:{}'.format(isbn)})

            if response.ok:
                try:
                    img = response.json().get('items', [])[0]['volumeInfo']['imageLinks']['thumbnail']
                except (IndexError, KeyError):
                    pass
                else:
                    file_content.append('')
                    file_content.append('![]({})'.format(img))

            file_content.append('**ISBN** {}'.format(content.isbn))

        for annotation in annotations:
            file_content.append('---')
            file_content.append('')
            file_content.append('> {}'.format(annotation))
            file_content.append('')

    if gist:
        filename = '{}.md'.format(isbn or 'mixed_quotes')
        files[filename] = {'content': '\n'.join(file_content)}

        response = requests.patch(
            '{}/{}'.format(GITHUB_GISTS_API, gist),
            headers={'Authorization': 'token {}'.format(github_token)},
            data=json.dumps({'files': files}))

        if response.ok:
            click.secho('successfully updated gist', fg='green')
        else:
            click.secho('something went wrong', fg='red')
