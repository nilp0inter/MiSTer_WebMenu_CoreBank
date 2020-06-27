# MiSTer_WebMenu_CoreBank

This repository contains a database of MiSTer cores and MRA files generated automatically every 10 minutes.

The database is available in JSON and curl-config format.

## Using the curl-config format to download all oficial cores & MRA files

### With `curl >= v7.66.0` (not available in MiSTer at the moment)

```console
$ mkdir _Test
$ cd _Test
$ curl -Z -C - -K <(curl -s -o - https://raw.githubusercontent.com/nilp0inter/MiSTer_WebMenu_CoreBank/master/db/users/MiSTer-devel.curl)
```

### Older versions of `curl`

```console
$ mkdir _Test
$ cd _Test
$ curl -C - -K <(curl -s -o - https://raw.githubusercontent.com/nilp0inter/MiSTer_WebMenu_CoreBank/master/db/users/MiSTer-devel.curl)
```
