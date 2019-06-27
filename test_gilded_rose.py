import unittest

from gilded_rose import Item, GildedRose


class GildedRoseTest(unittest.TestCase):
    def test_regular_item(self):
        # Quality and sell date should decrease by 1
        items = [Item(name="+5 Dexterity Vest", sell_in=10, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 9)
        self.assertEqual(items[0].quality, 19)

    def test_negative_quality(self):
        # The Quality of an item is never negative
        items = [Item(name="+5 Dexterity Vest", sell_in=10, quality=0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 0)

    def test_past_sell_degradation(self):
        # Once the sell by date has passed, Quality degrades twice as fast
        items = [Item(name="+5 Dexterity Vest", sell_in=-1, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 18)

    def test_quality_cap(self):
        # The Quality of an item is never more than 50
        items = [Item(name="Aged Brie", sell_in=-1, quality=55)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 50)

    def test_sulfuras(self):
        # "Sulfuras", being a legendary item, never has to be sold or decreases in Quality
        items = [
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
        ]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].sell_in, 0)
        self.assertEqual(items[0].quality, 80)
        self.assertEqual(items[1].sell_in, -1)
        self.assertEqual(items[1].quality, 80)

    def test_aged_brie(self):
        # "Aged Brie" actually increases in Quality the older it gets
        items = [Item(name="Aged Brie", sell_in=2, quality=0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 1)

    def test_backstage_pass_quality_cap(self):
        # Backstage pass should not go over quality 50
        items = [
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=49),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49),
        ]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 50)
        self.assertEqual(items[1].quality, 50)

    def test_backstage_pass_quality_stepping(self):
        # "Backstage passes", like aged brie, increases in Quality as its SellIn value approaches;
        # Quality increases by 2 when there are 10 days or less
        # Quality increases by 3 when there are 5 days or less
        items = [
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=10),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=10),
            Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=10),
        ]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 11)
        self.assertEqual(items[1].quality, 12)
        self.assertEqual(items[2].quality, 13)

    def test_backstage_pass_quality_expired(self):
        # Quality drops to 0 after the concert
        items = [Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=40)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 0)

    def test_conjured(self):
        # "Conjured" items degrade in Quality twice as fast as normal items
        items = [Item(name="Conjured Sword", sell_in=5, quality=40)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 38)

    def test_conjured_expired(self):
        # "Conjured" items should degrade four times as fast when expired
        items = [Item(name="Conjured Sword", sell_in=-1, quality=40)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(items[0].quality, 36)



if __name__ == '__main__':
    unittest.main()
