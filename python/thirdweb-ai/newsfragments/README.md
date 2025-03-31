# News Fragments

This directory contains "news fragments" which are short files that contain a small **RST**-formatted
text that will be added to the next version's changelog.

The news fragments are named `<issue_number>.<type>.md` where `<issue_number>` is the GitHub issue number
and `<type>` is one of:

* `feature`: New feature
* `bugfix`: Bug fix
* `performance`: Performance improvement
* `doc`: Documentation improvement
* `removal`: Feature removal or deprecation
* `misc`: Other changes

Make sure to use a brief and descriptive sentence for your news fragment. For example:

```
Add support for X feature.
```

When releasing a new version, the fragments will be automatically collected into the CHANGELOG by towncrier.
