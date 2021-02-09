# Flask File Sending Example Project

This project shows an example of file sending operation in Flask.
Also this project includes Blurhash encoding.

Server has two endpoints: `/file` and `/blurhash`.
`/file` endpoint supports `GET` and `POST` methods
which stands for getting and sending file. Only
images with these extensions can be sent: `png`, `jpg` and `jpeg`.
In `/blurhash` endpoint, you can get the Blurhash
encoded image in string. You can use this string to
show the blurry version of the actual image while it's
being downloaded.

Hope this project helps you, happy coding!

