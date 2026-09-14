# Linux Systems Folder Structure

This directory mirrors the distribution and version inventory defined by `../linux-systems.json`.

## Structure

```text
linux-systems/
├── ubuntu/
│   ├── 4.10-warty-warthog/
│   ├── 14.04-trusty-tahr/
│   ├── 16.04-xenial-xerus/
│   ├── 18.04-bionic-beaver/
│   ├── 20.04-focal-fossa/
│   ├── 22.04-jammy-jellyfish/
│   ├── 24.04-noble-numbat/
│   └── 26.04-plucky-puffin/
├── debian/
│   ├── 1.1-buzz/
│   ├── 9-stretch/
│   ├── 10-buster/
│   ├── 11-bullseye/
│   ├── 12-bookworm/
│   ├── 13-trixie/
│   └── 14-forky/
├── rhel/
│   ├── 2.1-as-pensacola/
│   ├── 7-maipo/
│   ├── 8-ootpa/
│   ├── 9-plow/
│   └── 10-bolkar/
├── fedora/
│   ├── 1-yarrow/
│   ├── 40/
│   ├── 41/
│   ├── 42/
│   ├── 43/
│   └── 44/
├── arch-linux/
│   └── rolling-release/
├── linux-mint/
│   ├── 1.0-ada/
│   ├── 20-ulyana/
│   ├── 21-vanessa/
│   └── 22-wilma/
└── opensuse/
    ├── 15.5-leap/
    ├── 15.6-leap/
    └── tumbleweed/
```

Each version directory is intended to contain a `META.md` describing the release and later distribution-specific administrative, kernel, package, filesystem, and locking information.

The source inventory is `../linux-systems.json`.