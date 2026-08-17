import unittest
from coding_trainer_ai.foundation import (
    AnalogyEngine,
    MathRosettaStone,
    TierPathManager,
    TierLevel,
)


class TestFoundationEngine(unittest.TestCase):

    def setUp(self):
        self.analogy_engine = AnalogyEngine()
        self.rosetta_stone = MathRosettaStone()
        self.tier_manager = TierPathManager()

    # -------------------------------------------------------------------------
    # Analogy Engine Tests & Edge Cases
    # -------------------------------------------------------------------------
    def test_analogy_cards_exist_and_valid(self):
        cards = self.analogy_engine.get_all()
        self.assertGreaterEqual(len(cards), 8, "Should have at least 8 default analogy cards.")
        for c in cards:
            self.assertTrue(c.id.startswith("analog_"))
            self.assertTrue(len(c.concept) > 0)
            self.assertTrue(len(c.non_cs_domain) > 0)
            self.assertTrue(len(c.analogy_explanation) > 0)
            self.assertTrue(len(c.technical_translation) > 0)
            self.assertTrue(len(c.example_snippet) > 0)

    def test_analogy_get_by_id(self):
        card = self.analogy_engine.get_by_id("analog_001")
        self.assertIsNotNone(card)
        self.assertIn("Pointers", card.concept)
        self.assertEqual(card.non_cs_domain, "History & Archival Cataloging")

    def test_analogy_get_by_invalid_id(self):
        card = self.analogy_engine.get_by_id("analog_invalid_999")
        self.assertIsNone(card)

    def test_analogy_search(self):
        results = self.analogy_engine.search("treaty")
        self.assertGreaterEqual(len(results), 1)
        self.assertTrue(any("Treaty" in r.analogy_title or "Treaty" in r.non_cs_domain for r in results))

    def test_analogy_search_no_match(self):
        results = self.analogy_engine.search("xyz_non_existent_term_123")
        self.assertEqual(len(results), 0)

    def test_analogy_filter_by_tag(self):
        cards = self.analogy_engine.filter_by_tag("c++")
        self.assertGreaterEqual(len(cards), 2)
        for c in cards:
            self.assertIn("c++", [t.lower() for t in c.tags])

    def test_analogy_filter_by_invalid_tag(self):
        cards = self.analogy_engine.filter_by_tag("non_existent_tag")
        self.assertEqual(len(cards), 0)

    # -------------------------------------------------------------------------
    # Math Rosetta Stone Tests & Edge Cases
    # -------------------------------------------------------------------------
    def test_greek_alphabet_dictionary(self):
        greek_dict = self.rosetta_stone.get_greek_alphabet()
        self.assertIn("∇ (Nabla)", greek_dict)
        self.assertIn("θ (Theta)", greek_dict)
        self.assertIn("σ (Sigma)", greek_dict)
        self.assertGreaterEqual(len(greek_dict), 10)

    def test_math_notation_cards_validity(self):
        cards = self.rosetta_stone.get_all_cards()
        self.assertGreaterEqual(len(cards), 4)
        for c in cards:
            self.assertTrue(len(c.symbol) > 0)
            self.assertTrue(len(c.name) > 0)
            self.assertTrue(len(c.domain) > 0)
            self.assertTrue(len(c.plain_english_breakdown) > 0)

    def test_decode_symbol(self):
        results = self.rosetta_stone.decode_symbol("gradient")
        self.assertGreaterEqual(len(results), 1)
        self.assertIn("∇L(θ)", results[0].symbol)

    def test_decode_symbol_no_match(self):
        results = self.rosetta_stone.decode_symbol("unknown_math_symbol_99")
        self.assertEqual(len(results), 0)

    # -------------------------------------------------------------------------
    # Tier Path Manager Tests & Edge Cases
    # -------------------------------------------------------------------------
    def test_tier_path_modules(self):
        modules = self.tier_manager.get_all_modules()
        self.assertGreaterEqual(len(modules), 2)

    def test_tier_level_display_names(self):
        for tier_val in [1, 2, 3, 4, 5]:
            t = TierLevel(tier_val)
            self.assertIn(f"Tier {tier_val}:", t.display_name)

    def test_module_has_all_five_tiers(self):
        for mod in self.tier_manager.get_all_modules():
            self.assertIsNotNone(mod)
            for tier_val in [1, 2, 3, 4, 5]:
                tier_enum = TierLevel(tier_val)
                self.assertIn(tier_enum, mod.tiers, f"Module {mod.id} missing tier {tier_val}")
                tier_obj = mod.tiers[tier_enum]
                self.assertTrue(len(tier_obj.title) > 0)
                self.assertTrue(len(tier_obj.explanation) > 0)
                self.assertTrue(len(tier_obj.uk_distinction_key_takeaway) > 0)

    def test_get_invalid_module_id(self):
        mod = self.tier_manager.get_module_by_id("invalid_module_xyz")
        self.assertIsNone(mod)


if __name__ == "__main__":
    unittest.main()
