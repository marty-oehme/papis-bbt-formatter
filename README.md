# papis-bbt-formatter

Formats reference keys in papis similarly to the (zotero plugin) `better-bibtex` keys, in the format `Name2008TitleShort`.
## Installation:

<!-- TODO set up pypi repository / explain git install path -->
You can install from pypi with `pip install git+https://git.martyoeh.me/Marty/papis-bbt-formatter.git`.

That's it! If you have papis and papis-bbt-formatter installed in the same environment (whether virtual or global),
everything should now be installed.

## Usage

In your papis configuration file (usually `~/.config/papis/config`), add the following under the main settings header:

```cfg
[settings]
formater = bbt
ref-format = bbt
```

For now, the ref-format also *has* to start with `bbt`. 

Formatted reference keys by default will look like:

`Harvey05briefhistoryneoliberalism` (for Harvey, D. (2005). A brief history of neoliberalism. Oxford New York: Oxford University Press.) 

or `Harvey22reflectionsacademiclife` (for Harvey, D. (2022). Reflections on an academic life. Human Geography, 15, 14–24. doi:10.1177/19427786211046291)

## Configuration

No configuration except for the above setup is required for the formatting to work,
but you can set a couple additional ones to customize the bevhavior to your liking:

### Title length

Currently, you can change the length that the `TitleShort` in `Name2008TitleShort` will be cut down to by setting
the maximum length in words `title-words=4` or in characters `title-chars=20` under the `[plugins.bbt-formatter]` section in your papis configuration file (usually located at `~/.config/papis/config`).

To set a maximum word length, do:

```cfg
[settings]
formater = bbt
ref-format = bbt

[plugins.bbt-formatter]
title-words = 4
```

In this case, the title will be shortened to 4 words maximum (the default),
change the number to shorten/lengthen to your preference.
Same idea for maximum character length:

```cfg
[plugins.bbt-formatter]
title-chars = 10
```

This will allow a maximum of 10 characters for the title.
Using both:

```cfg
[plugins.bbt-formatter]
title-words = 4
title-chars = 20
```

This will ensure a maximum of 4 words, however if they go more than 20 characters they will be cut off mid-word.
You can set either option to `-1` to turn it off:

```cfg
[plugins.bbt-formatter]
title-words = 4
title-chars = -1
```

This will ensure that a maximum of 4 words will be placed in the ref, but they do not have a maximum character length, 
so will always be fully written out (the default behavior if no title length options are provided).

---

For now this plugin is a rather simple adaption from [this](https://github.com/hrdl-github/papis/commit/b9b9c6eaa3de159e1b210174ef49e90a89271eb8) commit,
turned into an installable papis plugin and extended slightly.

If you spot a bug or have an idea feel free to open an issue.\
I might be slow to respond but will consider them all!

Pull requests are warmly welcomed.\
If they are larger changes or additions let's talk about them in an issue first.

Thanks for using my software ❤️
