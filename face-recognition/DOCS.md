# Home Assistant Custom Add-on: Face Recognition

This addon includes the [face_recognition package][face-reognition-package]
which allows recognizing and identifying faces from images.

## Installation

The installation of this add-on is pretty straightforward and not different in
comparison to installing any other Home Assistant add-on.

1. Add <https://github.com/engrbm87/HA-addons.git> to your Hass.io instance
   as a repository.
1. Search for the "Face Recognition" add-on in the Supervisor
   add-on store and install it.
1. Start the add-on
1. Check the logs of the add-on to see if everything went well.

## Usage

This addon including a webserver that provides the following endpoints:

- `GET /faces` - Returns a list of names for known faces that are stored.
  Faces are stored in `.npz` file that is saved under `/config/face_recognition`.

- `POST /faces` - Upload a new known face to store it in the database and use
  it for identification.

- `DELETE /faces` - Delete a stored known face by specifying the face name.
  (the name can be retrived from `GET /faces`)

- `POST /recognize` - Recognize and identify faces in uploaded image.
  (Identification requires having at least 1 known face stored to compare).
  Returns a dict of recognized faces with face locations. In case a face
  is identified the face name will be used as key instead of 'Unknown'.

For `POST /faces` it expects JSON in the following format:

```json
{
  "name": "FACE NAME",
  "image": "<base64 encoded image information>"
}
```

For `DELETE /faces` it expects JSON in the following format:

```json
{
  "name": "FACE NAME"
}
```

The result for `/faces` endpoint is returned as:

```json
{
  "results": "<list of face names successfully stored.>"
}
```

For `POST /recognize` it expects JSON in the following format:

```json
{
  "image": "<base64 encoded image information>"
}
```

The result is returned as:

```json
{
  "results": {
    "Unknown-1": [187, 1118, 295, 1011]
  }
}
```

In case of an error the response will include an `error` key with
error message.

## Configuration

### Option: `log_level`

The `log_level` option controls the level of log output by the addon and can
be changed to be more or less verbose, which might be useful when you are
dealing with an unknown issue. Possible values are:

- `debug`: Run webserver in debug mode.
- `error`: run webserver with debug mode turned off.

## Changelog & Releases

This repository keeps a change log using [GitHub's releases][releases]
functionality.

Releases are based on [Semantic Versioning][semver], and use the format
of `MAJOR.MINOR.PATCH`. In a nutshell, the version will be incremented
based on the following:

- `MAJOR`: Incompatible or major changes.
- `MINOR`: Backwards-compatible new features and enhancements.
- `PATCH`: Backwards-compatible bugfixes and package updates.

## Support

You can [open an issue here][issue] GitHub.

## License

MIT License

Copyright (c) 2021 Franck Nijhof

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[alpine-packages]: https://pkgs.alpinelinux.org/packages
[contributors]: https://github.com/hassio-addons/addon-appdaemon/graphs/contributors
[example-code]: https://github.com/engrbm87/appdaemon-with-face-recognition/tree/main/examples
[face-recognition-package]: https://github.com/ageitgey/face_recognition
[issue]: https://github.com/engrbm87/appdaemon-with-face-recognition/issues
[python-packages]: https://pypi.org/
[releases]: https://github.com/engrbm87/appdaemon-with-face-recognition/releases
[semver]: http://semver.org/spec/v2.0.0.htm
