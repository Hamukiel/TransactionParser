import unittest

from src.transactions.comparison import compare_iterables, compare_sentences


class ComparisonTests(unittest.TestCase):

    def test_compare_equal_string_iterables(self):
        input_a = 'TEST 1014'
        input_b = 'TEST 1014'
        expected_result = 1

        result = compare_iterables(input_a, input_b)
        assert result == expected_result

    def test_compare_similar_string_iterables(self):
        input_a = 'TEST 14'
        input_b = 'TEST 1014'
        expected_threshold = 0.5

        result = compare_iterables(input_a, input_b)
        assert result >= expected_threshold

    def test_compare_different_string_iterables(self):
        input_a = 'TEST 14'
        input_b = 'DIVE 1014'
        expected_threshold = 0.5

        result = compare_iterables(input_a, input_b)
        assert result < expected_threshold

    def test_compare_equal_list_iterables(self):
        input_a = ['TEST', '1014']
        input_b = ['TEST', '1014']
        expected_result = 1

        result = compare_iterables(input_a, input_b)
        assert result == expected_result

    def test_compare_similar_list_iterables(self):
        input_a = ['TEST', '14']
        input_b = ['TEST', '1014']
        expected_threshold = 0.5

        result = compare_iterables(input_a, input_b)
        assert result >= expected_threshold

    def test_compare_different_list_iterables(self):
        input_a = ['TEST', '14']
        input_b = ['DIVE', '1014']
        expected_threshold = 0.5

        result = compare_iterables(input_a, input_b)
        assert result < expected_threshold

    def test_compare_equal_sentences(self):
        input_a = 'PETCO ANIMAL SUPPLIES'
        input_b = 'PETCO ANIMAL SUPPLIES'
        expected_result = 1

        result = compare_sentences(input_a, input_b)
        assert result == expected_result

    def test_compare_similar_sentences(self):
        input_a = 'JACK IN THE BOX 92495'
        input_b = 'JACK IN THE BOX 57812'
        expected_threshold = 0.5

        result = compare_sentences(input_a, input_b)
        assert result >= expected_threshold

    def test_compare_different_sentences(self):
        input_a = 'THE HOME DEPOT 6132'
        input_b = "DILLARD'S"
        expected_threshold = 0.5

        result = compare_sentences(input_a, input_b)
        assert result < expected_threshold
