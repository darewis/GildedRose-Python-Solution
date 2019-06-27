class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if check_legendary(item):
                continue
            item.sell_in -= 1
            quality_delta = calculate_deltas(item)
            item.quality = validate_quality(item, quality_delta)


def check_legendary(item):
    """ Check if item is a Legendary """
    if item.name == 'Sulfuras, Hand of Ragnaros':
        return True
    return False


def validate_quality(item, delta):
    """ Return quality that follows rules given update delta """
    quality = item.quality - delta
    if item.name.startswith('Backstage pass') and item.sell_in < 0:
        # Backstage passes expire after concert
        quality = 0

    # ensure quality is within regular boundaries
    quality = max(0, quality)
    quality = min(50, quality)

    return quality


def calculate_deltas(item):
    """ Calculate delta to subtract from quality of item """
    quality_delta = 1

    if item.name == 'Aged Brie':
        # Aged Brie will increase in value
        quality_delta = -1
    elif item.name.startswith('Backstage pass'):
        # Backstage passes rate increases as concert date approaches
        if item.sell_in <= 5:
            quality_delta = -3
        elif item.sell_in <= 10:
            quality_delta = -2
        else:
            quality_delta = -1
    elif item.name.startswith('Conjured'):
        # Conjured items degrade twice as quickly
        quality_delta = 2

    if item.sell_in < 0 < quality_delta:
        # All items degrade twice as quickly when sell date passes
        quality_delta *= 2

    return quality_delta


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
