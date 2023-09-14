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

For now, the ref-format *has* to start with `bbt`.

### Title length

Currently, you can change the length that the `TitleShort` in `Name2008TitleShort` will be cut down to by setting
the maximum length in words or in characters.

To set a maximum word length, do:

```toml
[settings]
formater = bbt
ref-format = bbt[title-words=4]
```

In this case, the title will be shortened to 4 words maximum (the default),
change the number to shorten/lengthen to your preference.
Same idea for maximum character length:

```toml
[settings]
formater = bbt
ref-format = bbt[title-chars=10]
```

This will allow a maximum of 10 characters for the title.
Using both:

```toml
[settings]
formater = bbt
ref-format = bbt[title-words=4][title-chars=15]
```

This will ensure a maximum of 4 words, however if they go more than 20 characters they will be cut off mid-word.
You can set either option to `-1` to turn it off:

```toml
[settings]
formater = bbt
ref-format = bbt[title-words=4][title-chars=-1]
```

This will ensure that a maximum of 4 words will be placed in the ref, but they do not have a maximum character length, 
so will always be fully written out (the default behavior without title length options provided).

---

For now this plugin is a rather simple adaption from [this](https://github.com/hrdl-github/papis/commit/b9b9c6eaa3de159e1b210174ef49e90a89271eb8) commit,
turned into an installable papis plugin and extended slightly.

If you spot a bug or have an idea feel free to open an issue.\
I might be slow to respond but will consider them all!

Pull requests are warmly welcomed.\
If they are larger changes or additions let's talk about them in an issue first.

Thanks for using my software ❤️
