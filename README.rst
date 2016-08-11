kobo-sync
#############################


.. image:: https://travis-ci.org/elbaschid/kobo-sync.svg?branch=master
   :target: https://travis-ci.org/elbaschid/kobo-sync


Installation
------------

You can install this script using `pip` straight from github (it's not on 
PyPI for now)::

    $ pip install https://github.com/elbaschid/kobo-sync/archive/master.zip


Usage
-----

If you have your Kobo Reader connected to your Mac, you can easily extract
all the bookmarks and annotations by running::

    $ kobo_sync
    
And if you want to upload the extacted bookmarks to a gist, just add the 
gist SHA and it will update it with ``<ISBN>.md`` files for each book or
article you have annotated::
    
    $ kobo_sync --gist <gist SHA>

And if the ``KoboReader.sqlite`` database file is in a different location or
you are using a different system, you can specify a custom location like this::

    $ kobo_sync --db-file KoboReader.sqlite 


License
-------

This code is licensed under the `MIT License`_.

.. _`MIT License`: https://github.com/elbaschid/kobo-sync/blob/master/LICENSE
