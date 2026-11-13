import tempfile
import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


APP_DIR = Path(__file__).resolve().parents[1]


class FlashcardsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.wrongs = Path(self.temp.name) / "wrongs.txt"
        source = (APP_DIR / "avionics_flashcard_app.py").read_text(encoding="utf-8")
        source = source.replace("APP_DIR = Path(__file__).resolve().parent", f"APP_DIR = Path({str(APP_DIR)!r})")
        source = source.replace('WRONGS_PATH = APP_DIR / "wrongs.txt"', f"WRONGS_PATH = Path({str(self.wrongs)!r})")
        self.app = AppTest.from_string(source).run()
        self.assertFalse(self.app.exception)

    def click(self, label):
        next(button for button in self.app.button if button.label == label).click().run()
        self.assertFalse(self.app.exception)

    def test_all_452_cards_can_be_completed(self):
        self.app.radio[0].set_value("全部混合練習").run()
        deck = self.app.session_state.deck
        self.assertEqual(len(deck), 452)
        self.assertEqual(len({(unit, term) for unit, term, meaning in deck}), 452)
        self.assertEqual(len({unit for unit, term, meaning in deck}), 30)
        for _ in range(452):
            unit, term, meaning = self.app.session_state.deck[self.app.session_state.card_index]
            question = next(m.value for m in self.app.markdown if m.value.startswith("### "))
            self.assertNotEqual(question, f"### 🔤 {term}")
            self.assertGreater(len(question), 15)
            self.assertFalse(any(b.label == "✅ 我知道" for b in self.app.button))
            self.click("👀 顯示解釋")
            self.click("✅ 我知道")
        self.assertEqual(self.app.metric[0].value, "100%")
        self.assertFalse(self.wrongs.exists())
        self.click("🔁 重練這個單元")
        self.assertEqual(self.app.session_state.card_index, 0)
        self.assertEqual(len(self.app.session_state.deck), 452)

    def test_wrong_review_and_unit_switch(self):
        self.app.selectbox[0].select_index(9).run()
        self.assertEqual(len(self.app.session_state.deck), 6)
        wrong = self.app.session_state.deck[0]
        self.click("👀 顯示解釋")
        self.click("❌ 還不熟")
        for _ in range(5):
            self.click("👀 顯示解釋")
            self.click("✅ 我知道")
        self.assertEqual(self.app.metric[0].value, "83%")
        self.assertIn(wrong[1], self.wrongs.read_text(encoding="utf-8"))
        self.click("只重練本次不熟的卡")
        self.assertEqual(self.app.session_state.deck, [wrong])
        self.click("👀 顯示解釋")
        self.click("❌ 還不熟")
        self.app.radio[0].set_value("歷史錯題複習").run()
        self.assertEqual(self.app.session_state.deck, [wrong])
        self.assertEqual(self.app.session_state.card_index, 0)
        self.app.radio[0].set_value("分單元練習").run()
        self.assertEqual(self.app.session_state.card_index, 0)
        self.assertEqual(len(self.app.session_state.deck), 17)

    def test_empty_history(self):
        self.app.radio[0].set_value("歷史錯題複習").run()
        self.assertFalse(self.app.exception)
        self.assertIn("目前沒有歷史錯題", self.app.info[0].value)

    def test_r_has_body_rate_context_without_revealing_answer(self):
        self.app.selectbox[0].select_index(6).run()
        card = next(card for card in self.app.session_state.deck if card[1] == "R")
        self.app.session_state.deck = [card]
        self.app.run()
        question = next(m.value for m in self.app.markdown if m.value.startswith("### "))
        self.assertIn("機體座標系", question)
        self.assertIn("角速度分量 r", question)
        self.assertNotIn("Yaw Rate", question)
        self.assertFalse(any("Yaw Rate" in m.value for m in self.app.markdown))
        self.click("👀 顯示解釋")
        self.assertTrue(any("Yaw Rate" in m.value for m in self.app.markdown))

    def test_every_card_has_a_question_and_banks_match(self):
        lines = (APP_DIR / "alias.txt").read_text(encoding="utf-8").splitlines()
        pending = False
        questions = 0
        for line in lines:
            if line.startswith("? "):
                self.assertFalse(pending)
                pending = True
                questions += 1
            elif line and not line.startswith(("#", "[")):
                self.assertTrue(pending, line)
                pending = False
        self.assertFalse(pending)
        self.assertEqual(questions, 452)
        # The standalone repo can run without the course workspace's copy.
        workspace_copy = APP_DIR.parent / "alias.txt"
        if workspace_copy.exists():
            self.assertEqual(workspace_copy.read_bytes(), (APP_DIR / "alias.txt").read_bytes())

    def test_failed_save_keeps_session_review(self):
        self.wrongs.mkdir()
        self.click("👀 顯示解釋")
        self.click("❌ 還不熟")
        self.assertEqual(len(self.app.session_state.wrong_cards), 1)
        self.assertEqual(self.app.session_state.card_index, 1)
        self.assertTrue(self.app.warning)

    def test_extended_mode_and_offline_downloads(self):
        self.assertEqual(len(self.app.get("download_button")), 2)
        self.app.radio[0].set_value("作業與申論混合").run()
        self.assertFalse(self.app.exception)
        self.assertEqual(len(self.app.session_state.deck), 300)
        self.assertTrue(all(term.startswith("HW-") for unit, term, answer in self.app.session_state.deck))
        card = next(c for c in self.app.session_state.deck if c[1] == "HW-ALT-01")
        self.app.session_state.deck = [card]
        self.app.run()
        self.click("👀 顯示解釋")
        self.assertTrue(any("架構：" in m.value for m in self.app.markdown))
        self.assertTrue(any("回授：" in m.value for m in self.app.markdown))


if __name__ == "__main__":
    unittest.main()
