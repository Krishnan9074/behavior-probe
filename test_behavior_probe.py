import json
import tempfile
import unittest
from pathlib import Path

from behavior_probe import (StudentRule, baseline, generate, grade,
                            read_json, start_session, student_answer, probe)


class TestBenchmark(unittest.TestCase):
    def test_all_basic_rules(self):
        # 53-27; correct 26. Each procedural rule makes a systematic error.
        self.assertEqual(student_answer(53, 27, StudentRule('smaller_from_larger')), 34)
        self.assertEqual(student_answer(53, 27, StudentRule('forget_decrement')), 36)
        self.assertEqual(student_answer(53, 27, StudentRule('write_zero')), 30)
        self.assertEqual(student_answer(100, 1, StudentRule('zero_bridge')), 109)
        # A case without borrowing stays correct even for buggy students.
        self.assertEqual(student_answer(85, 21, StudentRule('write_zero')), 64)

    def test_generated_data_and_grading(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / 'cases'
            generate(root, 123, 2)
            pub = read_json(root / 'public' / 'S001.json')
            priv = read_json(root / 'private' / 'S001.json')
            self.assertEqual(len(pub['test_questions']), 40)
            self.assertNotIn('rule', pub)
            self.assertEqual(sum(x['student_is_wrong'] for x in priv['test_answers'].values()), 20)
            start_session(root, 'S001', 3, 'trial_01')
            probe(root, 'trial_01', 502, 178)
            pth = Path(t) / 'baseline.json'
            baseline(root, 'S001', pth)
            report = grade(root, 'trial_01', pth)
            self.assertEqual(report['probes_used'], 1)
            self.assertEqual(report['primary_wrong_answer_accuracy'], 0.0)
            self.assertEqual(report['correct_answer_accuracy_diagnostic'], 1.0)

    def test_generator_is_reproducible(self):
        with tempfile.TemporaryDirectory() as t:
            a, b = Path(t) / 'a', Path(t) / 'b'
            generate(a, 17, 1)
            generate(b, 17, 1)
            self.assertEqual((a/'public/S001.json').read_bytes(), (b/'public/S001.json').read_bytes())


if __name__ == '__main__':
    unittest.main()
