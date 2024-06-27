[![Tests](https://github.com/matthiasgi/directorium/workflows/Testing%20code/badge.svg)](https://github.com/matthiasgi/directorium/actions?query=workflow:"Testing+code")
[![Publish Package](https://github.com/matthiasgi/directorium/workflows/Upload%20Python%20Package/badge.svg)](https://github.com/matthiasgi/directorium/actions?query=workflow:"Upload+Python+Package")
[![GitHub release](https://img.shields.io/github/release/matthiasgi/directorium?include_prereleases=&sort=semver&color=blue)](https://github.com/matthiasgi/directorium/releases/)
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)
[![issues - directorium](https://img.shields.io/github/issues/matthiasgi/directorium)](https://github.com/matthiasgi/directorium/issues)

# directorium

A wrapper package for the public API of https://eucharistiefeier.de/lk/. It is able to provide information from the liturgical calendar such as liturgical color and lectures. To start with the package just run:
```shell
pip install directorium
```

## Getting started

A sample usage would be:
```python
from datetime import date
from directorium import Directorium

directorium = Directorium.from_request()
today = date.today()
events = directorium.get_date(today)
print(events)
```

## Documentation

An automatically created documentation is available on [https://matthiasgi.github.io/directorium/](the GitHub Pages of this project).

## Acknowledgments
Thanks a lot to the [Salesians of Don Bosco](https://www.donbosco.de/) for providing the API!

## License

Released under [MIT](/LICENSE) by [@matthiasgi](https://github.com/matthiasgi).
