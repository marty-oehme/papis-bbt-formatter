# papis-bbt-formatter

Formats reference keys in papis similarly to the (zotero plugin) `better-bibtex` keys, in the format `Name2008TitleShort`.
## Installation:

<!-- TODO set up pypi repository / explain git install path -->
You can install from pypi with `pip install git+https://git.martyoeh.me/Marty/papis-bbt-formatter.git`.

That's it! If you have papis and papis-bbt-formatter installed in the same environment (whether virtual or global),
everything should now be installed.

## Usage:

In your papis configuration file (usually `~/.config/papis/config`), add the following under the main settings header:

```toml
[settings]
formater = bbt
ref-format = bbt
```

For now, the ref-format is simply `bbt` as well, though should I further develop this plugin (with additional options),
that settings will surely change.

Currently, you can change the length that the `TitleShort` in `Name2008TitleShort` will be cut down to by setting:

```toml
[settings]
formater = bbt
ref-format = bbt[4]
```

In this case, the title will be shortened to 4 words maximum (the default), change the number to shorten/lengthen to your preference.

This plugin is a rather simple adaption from [this](https://github.com/hrdl-github/papis/commit/b9b9c6eaa3de159e1b210174ef49e90a89271eb8) commit,
turned into an installable papis plugin and extended slightly for now.

---

If you spot a bug or have an idea feel free to open an issue.\
I might be slow to respond but will consider them all!

Pull requests are warmly welcomed.\
If they are larger changes or additions let's talk about them in an issue first.

Thanks for using my software ❤️
