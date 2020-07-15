# 4chan Thread Images

Extract all the images from a 4chan thread.

## Details

Extract images (PNGs and JPGs) from a 4chan thread.

A thread's URL looks like this (sample): https://boards.4channel.org/w/thread/2159787

Usage:

    $ ./get_thread_list.py <4chan_thread_url>

The image list will be saved to a file called `down.txt`.
Copy `down.txt` to a folder and issue the following command:

    $ wget -i down.txt

to download all the images.
