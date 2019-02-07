Uploading content on Funkwhale
==============================

To upload content on any Funkwhale instance, you need:

1. An account on that instance
2. :ref:`Storage space <upload-storage>`
3. :ref:`A library <upload-library>`
4. :ref:`Properly tagged files <upload-tagging>`
5. :ref:`To upload your files <upload-upload>`

In this document, we'll guide you through steps 2 to 5.

.. _upload-storage:

Storage space
-------------

Once you have an account on a Funkwhale instance, as a user, you are granted the
default upload quota (1GB by default). This default quota can be increased,
reduced or completely removed by your instance admins depending on their policy.

Additionnaly, instance admins can grant you storage space manually. Get in touch with them
if you'd like some additionnal storage space.

You can view your current quota and usage at any time by visiting ``/content/libraries/`` on your instance,
or clicking the "Add content" link in the sidebar, then visiting the "Upload audio content" section.

.. _upload-library:

Creating a library
------------------

In Funkwhale's world, a library is a collection of audio files with an associated visibility level. A library can either be:

- Public: anyone can follow the library to automatically access its content (including users on other instances)
- Local: other users from your instance can follow the library to automatically access its content
- Private: nobody will access the library content

Regardless of this visibility settings, you can share the library link to specific users
and accept their follow request in order to grant then access to its content. Typically, this
is useful when you have a private library you want to share with friends or family.

You can create your first library by visiting ``/content/libraries/`` or clicking the "Add content" link in the sidebar, then visiting the "Upload audio content" section.

Before you upload your content, you need to know the content audience and license:

- If the content is under an open license (like Creative Commons licenses), it's usually fine to upload it in a public library
- If you are uploading content purchased from other platforms or stores, you should upload it in a private library

.. note::

    As a rule of thumb, only use public and local libraries for content for which you own the copyright or for content you know you can share with a wider audience.

.. _upload-tagging:

Tagging files
-------------

Funkwhale relies on embedded file metadata (also known as tags) to infer the artist,
album and track associated with a given upload. Most stores and platforms include
those tags by default, but it's possible the tags are missing or incomplete, in which case
Funkwhale will not be able to process the upload and display an error.

The minimum required tags are:

- Title
- Artist
- Album

However, Funkwhale can understand and use additionnal tags to enhance user experience and display more information. The full list of supported tags is available below:

+----------------------------------+--------------------------------------------+---------------------------------------------------------------+
| Name                             | Example value                              | Description                                                   |
+----------------------------------+--------------------------------------------+---------------------------------------------------------------+
| ``Title`` (required)             | ``Letting you``                            | The track title                                               |
|                                  |                                            |                                                               |
+----------------------------------+--------------------------------------------+---------------------------------------------------------------+
| ``Album`` (required)             | ``The Slip``                               | The album title                                               |
|                                  |                                            |                                                               |
+----------------------------------+--------------------------------------------+---------------------------------------------------------------+
| ``Artist`` (required)            | ``Nine Inch Nails``                        | The artist name                                               |
|                                  |                                            |                                                               |
+----------------------------------+--------------------------------------------+---------------------------------------------------------------+
| ``Album artist``                 | ``Trent Reznor``                           | The album artist name (can be different than the track        |
|                                  |                                            | artist)                                                       |
|                                  |                                            |                                                               |
+----------------------------------+--------------------------------------------+---------------------------------------------------------------+
| ``Track number``                 | ``4``                                      | The position of the track in the album/release                |
|                                  |                                            |                                                               |
+----------------------------------+--------------------------------------------+---------------------------------------------------------------+
| ``Disc number``                  | ``1``                                      | The disc number (in case of multi-disc albums)                |
|                                  |                                            |                                                               |
+----------------------------------+--------------------------------------------+---------------------------------------------------------------+
| ``Date``                         | ``2019``                                   | The release date of the track or album                        |
|                                  |                                            |                                                               |
|                                  |                                            |                                                               |
+----------------------------------+--------------------------------------------+---------------------------------------------------------------+
| ``License``                      | ``CC-BY 3.0: http://creativecommons        | The license associated with this work. The first found URL    |
|                                  | .org/licenses/cc-by/3.0/``                 | will be checked against `our list of supported licenses`_     |
|                                  |                                            |                                                               |
+----------------------------------+--------------------------------------------+---------------------------------------------------------------+
| ``Copyright``                    | ``CC-BY 3.0: http://creativecommons        | The license associated with this work. The first found URL    |
|                                  | .org/licenses/cc-by/3.0/``                 | will be checked against `our list of supported licenses`_.    |
|                                  |                                            | Used if no license found in the License tag                   |
|                                  |                                            |                                                               |
+----------------------------------+--------------------------------------------+---------------------------------------------------------------+
| ``Pictures``                     |                                            | The first embeded picture found will be used as the album     |
|                                  |                                            | covers                                                        |
|                                  |                                            |                                                               |
+----------------------------------+--------------------------------------------+---------------------------------------------------------------+
| ``MusicBrainz Recording ID``     | ``99244237-850b-4a93-904d-57305bcadb4e``   | The MusicBrainz ID for this recording                         |
|                                  |                                            |                                                               |
+----------------------------------+--------------------------------------------+---------------------------------------------------------------+
| ``MusicBrainz Album ID``         | ``bca982fd-ab73-3c9f-ad07-9104a4f53a32``   | The MusicBrainz ID for this album                             |
|                                  |                                            |                                                               |
+----------------------------------+--------------------------------------------+---------------------------------------------------------------+
| ``MusicBrainz Artist ID``        | ``b7ffd2af-418f-4be2-bdd1-22f8b48613da``   | The MusicBrainz ID for this artist                            |
|                                  |                                            |                                                               |
+----------------------------------+--------------------------------------------+---------------------------------------------------------------+
| ``MusicBrainz Album Artist ID``  | ``b7ffd2af-418f-4be2-bdd1-22f8b48613da``   | The MusicBrainz ID for this album artist                      |
+----------------------------------+--------------------------------------------+---------------------------------------------------------------+

.. _our list of supported licenses: https://dev.funkwhale.audio/funkwhale/funkwhale/blob/develop/api/tests/music/licenses.json

The easiest way to inspect and edit file tags is with `MusicBrainz Picard <https://picard.musicbrainz.org/>`_, a free
software, that works on Windows, MacOS and Linux. Picard is able to automatically tag many files,
and include non-necessary but nice to have information, such as album covers.

.. _upload-upload:

Uploading your files
--------------------

Once you've chose the library and have properly tagged files, you can start the actual upload.
Simply visit ``/content/libraries/`` or click the "Add content" link in the sidebar, then visit the "Upload audio content" section. Click on
the "Upload" button next to the library of your choice, and follow the instructions.

You can queue as many files as you want for the upload, simply leave your browser window open on the upload page
until all files are uploaded.

By default, Funkwhale accepts files up to 100MB in size, but this limit can be increased or reduced
by instance admins.

Once uploaded, your files should be processed shortly. It's usually a matter of seconds, but
can vary depending on server load.