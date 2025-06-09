# papis-bbt-formatter

Formats reference keys in papis similarly to the (zotero plugin) `better-bibtex` keys, in the format `Name2008TitleShort`.

## Installation

<!-- TODO set up pypi repository / explain git install path -->

You can install from pypi with `pip install git+https://git.martyoeh.me/Marty/papis-bbt-formatter.git`.

That's it! If you have papis and papis-bbt-formatter installed in the same environment (whether virtual or global),
everything should now be installed.

<!-- markdownlint-disable MD033 -->
<details>
<summary>Virtual environment setup</summary>

Depending on the way you set up your virtual environments, plugins like this can be _injected_ by the virtual environment manager.

For example, using `uv`, you can install papis to be accessible globally together with papis-bbt-formatter in the following way:

```bash
uv tool install --with git+https://git.martyoeh.me/Marty/papis-bbt-formatter.git papis
```

Or, with `pipx`:

```bash
pipx install papis
pipx inject papis git+https://git.martyoeh.me/Marty/papis-bbt-formatter.git
```

</details>
<!-- markdownlint-enable MD033 -->

## Usage

In your papis configuration file (usually `~/.config/papis/config`), add the following under the main settings header:

```cfg
[settings]
formater = bbt
ref-format = bbt:
```

For now, the ref-format also _has_ to start with `bbt:`.

Formatted reference keys by default will look like:

`Harvey05briefhistoryneoliberalism` (for Harvey, D. (2005). A brief history of neoliberalism. Oxford New York: Oxford University Press.)

or `Harvey22reflectionsacademiclife` (for Harvey, D. (2022). Reflections on an academic life. Human Geography, 15, 14–24. doi:10.1177/19427786211046291)

## Configuration

No configuration except for the above setup is required for the formatting to work,
but you can set a couple additional ones to customize the behavior to your liking.
Listed below are all options with their defaults:

```cfg
[settings]
formater = bbt
ref-format = bbt:

[plugins.bbt]
default-formatter = python
full-year = False
title-words = 4
title-chars = -1
```

### Full year

You can specifiy whether the reference should contain the full 4-digit year representation (i.e. `1997`, `2018`) or just a shortened 2-digit version (`97`, `18`):

```cfg
[plugins.bbt]
full-year = True
```

This will insert the full 4-digit publication year instead of the (default) shortened version.

### Title length

You can change the length that the `TitleShort` in `Name2008TitleShort` will be cut down to by setting
the maximum length in words `title-words=4` or in characters `title-chars=20` under the `[plugins.bbt]` section in your papis configuration file (usually located at `~/.config/papis/config`).

To set a maximum word length, do:

```cfg
[plugins.bbt]
title-words = 4
```

In this case, the title will be shortened to 4 words maximum (the default),
change the number to shorten/lengthen to your preference.
Same idea for maximum character length:

```cfg
[plugins.bbt]
title-chars = 10
```

This will allow a maximum of 10 characters for the title.
Using both:

```cfg
[plugins.bbt]
title-words = 4
title-chars = 20
```

This will ensure a maximum of 4 words, however if they go more than 20 characters they will be cut off mid-word.
You can set either option to `-1` to turn it off:

```cfg
[plugins.bbt]
title-words = 4
title-chars = -1
```

This will ensure that a maximum of 4 words will be placed in the ref, but they do not have a maximum character length,
so will always be fully written out (the default behavior if no title length options are provided).

### Fallback formatter

For anything that is not a reference, use this formatter.
Basically, put the formatter you had before switching to bbt here:

```cfg
[plugins.bbt]
default-formatter = jinja2
```

Can be any of the installed papis formatters, including custom ones
(though usually it will be `python`, which is also the default setting).

---

This plugin is a fairly simple adaption from [this](https://github.com/hrdl-github/papis/commit/b9b9c6eaa3de159e1b210174ef49e90a89271eb8) commit,
turned into an installable papis plugin and extended a bit.

If you spot a bug or have an idea feel free to open an issue.\
I might be slow to respond but will consider them all!

Pull requests are warmly welcomed.\
If they are larger changes or additions let's talk about them in an issue first.

Thanks for using my software ❤️
