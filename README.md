# Scrapper the Gatherer: A Magic the Gathering Dataset

![](./assets/430547_img.jpeg)

**Goal**: Create a Magic the Gathering dataset from the website The Gatherer.

## What project includes?

* `scrapper.py`: retrieve a card type and populate the file `card_database.csv` with the following information:
  * id: card id used by The Gatherer card database
  * type: card type (e.g. monster, enchantment, artifact, etc)
  * subtype: card subtype (e.g. elf, goblin, etc)
  * url: link to a website with card information
<br></br>
* `card_retriever.py`: Given a card url retrieve the whole card information into two sources:
  * A csv storing the card information such as description, abilities, mana cost, etc.
  * An image of the card
<br></br>
* `data/`: folder that includes all the data curated:
  * `card_directory.csv`:
  * `card_info.csv`: features with the text that have each card
  * `card_type/card_subtype`: each folder contain the card images

## Disclaimer

The Magic Database

Regard [The Gatherer legal terms](https://company.wizards.com/en/legal/terms), section
2, article "2.1 License":

> (i) Data mining: Use any unauthorized means, process, or software that accesses, collects, reads, intercepts, monitors, data scrapes including without limitation, agents, robots, scripts, or spiders; or mines information (including reverse look-up or attempted tracing of Registration Data in any way and for any reason);

