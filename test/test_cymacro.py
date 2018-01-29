import os

from unittest import TestCase
from distutils.core import Extension

import cymacro as cm
import settings

from cymacro import N_HEADER_LINES as N_HDR


TEST_RESOURCES_PATH = settings.ROOT_PATH + '/test/resources'


class TestFileExpander(TestCase):

    # Uses

    def test_file_expander_finds_c_like_definition(self):
        path = TEST_RESOURCES_PATH + '/c_like_basic_definition.pyx.cm'
        expander = cm.FileExpander.from_path(path)
        expander()

        self.assertIn('TEST_VALUE', expander.definitions)
        self.assertEqual('1234', expander.definitions['TEST_VALUE'].body)

    def test_file_expander_finds_c_like_definition2(self):
        path = TEST_RESOURCES_PATH + '/c_like_basic_definition2.pyx.cm'
        expander = cm.FileExpander.from_path(path)
        expander()

        self.assertIn('TEST_VALUE', expander.definitions)
        self.assertEqual('1234', expander.definitions['TEST_VALUE'].body)

    def test_multi_line_c_like_macro_is_found(self):
        path = TEST_RESOURCES_PATH + '/c_like_multi_definition.pyx.cm'
        expander = cm.FileExpander.from_path(path)
        expander()

        self.assertIn('FOO', expander.definitions)
        self.assertEqual(
            'def foo(): \n    print(\'stuff\')',
            expander.definitions['FOO'].body
        )

    def test_file_expander_finds_py_like_definition(self):
        path = TEST_RESOURCES_PATH + '/py_like_basic_definition.pyx.cm'
        expander = cm.FileExpander.from_path(path)
        expander()

        self.assertIn('TEST_VALUE', expander.definitions)
        self.assertEqual('1234', expander.definitions['TEST_VALUE'].body)

    def test_file_expander_finds_multi_line_py_like_definition(self):
        path = TEST_RESOURCES_PATH + '/py_like_multi_definition.pyx.cm'
        expander = cm.FileExpander.from_path(path)
        expander()

        self.assertIn('FOO', expander.definitions)
        self.assertEqual(
            'def foo():\n    print(\'stuff\')\n',
            expander.definitions['FOO'].body
        )

    def test_file_expander_finds_and_expands_macro_use(self):
        path = TEST_RESOURCES_PATH + '/basic_use.pyx.cm'
        o = TEST_RESOURCES_PATH + '/basic_use.pyx'

        try:
            expander = cm.FileExpander.from_path(path, o)
            expander.definitions['TEST_VALUE'] = cm.Macro('TEST_VALUE', '1234')
            expander()

            self.assertTrue(os.path.exists(o), 'Out file was not created.')
            with open(o, 'r+') as f:
                lines = f.readlines()
                self.assertEqual('1234\n', lines[4 + N_HDR])
        finally:
            try:
                os.remove(o)
            except FileNotFoundError:
                pass

    def test_file_expander_finds_and_expands_indented_macro_use(self):
        path = TEST_RESOURCES_PATH + '/indented_use.pyx.cm'
        o = TEST_RESOURCES_PATH + '/indented_use.pyx'

        try:
            expander = cm.FileExpander.from_path(path, o)
            expander.definitions['TEST_VALUE'] = cm.Macro('TEST_VALUE', '1234')
            expander()

            self.assertTrue(os.path.exists(o), 'Out file was not created.')
            with open(o, 'r+') as f:
                lines = f.readlines()
                self.assertEqual('    1234\n', lines[5 + N_HDR])
        finally:
            try:
                os.remove(o)
            except FileNotFoundError:
                pass

    def test_file_expander_finds_and_expands_multi_line_macro_use(self):
        path = TEST_RESOURCES_PATH + '/multi_use.pyx.cm'
        o = TEST_RESOURCES_PATH + '/multi_use.pyx'

        try:
            expander = cm.FileExpander.from_path(path, o)
            expander.definitions['FOO'] = cm.Macro(
                'FOO',
                'def foo(): \n    print(\'stuff\')'
            )
            expander()

            self.assertTrue(os.path.exists(o), 'Out file was not created.')
            with open(o, 'r+') as f:
                lines = f.readlines()
                self.assertEqual('def foo(): \n', lines[4 + N_HDR])
                self.assertEqual('    print(\'stuff\')\n', lines[5 + N_HDR])
        finally:
            try:
                os.remove(o)
            except FileNotFoundError:
                pass

    def test_file_expander_expands_multi_line_indented_macro_correctly(self):
        path = TEST_RESOURCES_PATH + '/indented_multi_use.pyx.cm'
        o = settings.ROOT_PATH + '/test/resources/indented_multi_use.pyx'

        try:
            expander = cm.FileExpander.from_path(path, o)
            expander.definitions['FOO'] = cm.Macro(
                'FOO',
                'def foo(): \n    print(\'stuff\')'
            )
            expander()

            self.assertTrue(os.path.exists(o), 'Out file was not created.')
            with open(o, 'r+') as f:
                lines = f.readlines()
                self.assertEqual('    def foo(): \n', lines[5 + N_HDR])
                self.assertEqual('        print(\'stuff\')\n',
                                 lines[6 + N_HDR])
        finally:
            try:
                os.remove(o)
            except FileNotFoundError:
                pass

    def test_multi_word_macro_expands_correctly(self):
        path = TEST_RESOURCES_PATH + '/wordy_use.pyx.cm'
        o = settings.ROOT_PATH + '/test/resources/wordy_use.pyx'

        try:
            expander = cm.FileExpander.from_path(path, o)
            expander.definitions['WORDY'] = cm.Macro(
                'WORDY',
                '123 + 456'
            )
            expander()

            self.assertTrue(os.path.exists(o), 'Out file was not created.')
            with open(o, 'r+') as f:
                lines = f.readlines()
                self.assertEqual('123 + 456\n', lines[4 + N_HDR])
        finally:
            try:
                os.remove(o)
            except FileNotFoundError:
                pass

    def test_nested_macro_use_expands_correctly(self):
        path = TEST_RESOURCES_PATH + '/nested_use.pyx.cm'
        o = TEST_RESOURCES_PATH + '/nested_use.pyx'

        try:
            expander = cm.FileExpander.from_path(path, o)
            expander.definitions['FOO'] = cm.Macro(
                'FOO',
                'print(MONTY + PYTHON)'
            )
            expander.definitions['MONTY'] = cm.Macro(
                'MONTY',
                "'No one expects '"
            )
            expander.definitions['PYTHON'] = cm.Macro(
                'PYTHON',
                "'The Spanish Inquisition'"
            )
            expander()

            self.assertTrue(os.path.exists(o), 'Out file was not created.')
            with open(o, 'r+') as f:
                lines = f.readlines()
                self.assertEqual(
                    "print('No one expects ' + 'The Spanish Inquisition')\n",
                    lines[4 + N_HDR]
                )
        finally:
            try:
                os.remove(o)
            except FileNotFoundError:
                pass

    def test_single_quotes_are_copied_correctly(self):
        path = TEST_RESOURCES_PATH + '/quote_test.pyx.cm'
        o = settings.ROOT_PATH + '/test/resources/quote_test.pyx'

        try:
            expander = cm.FileExpander.from_path(path, o)
            expander()

            self.assertTrue(os.path.exists(o), 'Out file was not created.')
            with open(o, 'r+') as f:
                lines = f.readlines()
                self.assertEqual('"single char quotes"\n', lines[4 + N_HDR])
        finally:
            try:
                os.remove(o)
            except FileNotFoundError:
                pass

    def test_triple_quotes_are_copied_correctly(self):
        path = TEST_RESOURCES_PATH + '/wordy_use.pyx.cm'
        o = settings.ROOT_PATH + '/test/resources/wordy_use.pyx'

        try:
            expander = cm.FileExpander.from_path(path, o)
            expander()

            self.assertTrue(os.path.exists(o), 'Out file was not created.')
            with open(o, 'r+') as f:
                lines = f.readlines()
                self.assertEqual('"""\n', lines[2 + N_HDR])
        finally:
            try:
                os.remove(o)
            except FileNotFoundError:
                pass

    def test_backslashes_are_copied_correctly(self):
        path = TEST_RESOURCES_PATH + '/backslash.pyx.cm'
        o = settings.ROOT_PATH + '/test/resources/backslash.pyx'

        try:
            expander = cm.FileExpander.from_path(path, o)
            expander()

            self.assertTrue(os.path.exists(o), 'Out file was not created.')
            with open(o, 'r+') as f:
                lines = f.readlines()
                self.assertEqual('a = \\\n', lines[4 + N_HDR])
                self.assertEqual('    5 + 6\n', lines[5 + N_HDR])
        finally:
            try:
                os.remove(o)
            except FileNotFoundError:
                pass

    def test_brackets_are_copied_correctly(self):
        path = TEST_RESOURCES_PATH + '/brackets.pyx.cm'
        o = settings.ROOT_PATH + '/test/resources/brackets.pyx'

        try:
            expander = cm.FileExpander.from_path(path, o)
            expander()

            self.assertTrue(os.path.exists(o), 'Out file was not created.')
            with open(o, 'r+') as f:
                lines = f.readlines()
                self.assertEqual('(\'foo\')\n', lines[4 + N_HDR])
        finally:
            try:
                os.remove(o)
            except FileNotFoundError:
                pass

    def test_comments_are_copied_correctly(self):
        file_name = 'comment'
        path = TEST_RESOURCES_PATH + '/' + file_name + '.pyx.cm'
        o = TEST_RESOURCES_PATH + '/' + file_name + '.pyx'

        try:
            expander = cm.FileExpander.from_path(path, o)
            expander()

            self.assertTrue(os.path.exists(o), 'Out file was not created.')
            with open(o, 'r+') as f:
                lines = f.readlines()
                self.assertEqual('def foo():  # does stuff\n',
                                 lines[4 + N_HDR])
                self.assertEqual('    pass\n', lines[5 + N_HDR])
        finally:
            try:
                os.remove(o)
            except FileNotFoundError:
                pass

    def test_file_expander_can_clean_created_files(self):
        path = TEST_RESOURCES_PATH + '/clean_test.pyx.cm'
        o = TEST_RESOURCES_PATH + '/clean_test.pyx'

        try:
            expander = cm.FileExpander.from_path(path, o)
            expander()

            self.assertTrue(os.path.exists(o), 'Out file was not created.')

            expander.clean()
            self.assertFalse(os.path.exists(o), 'Out file was not removed')
        finally:
            try:
                os.remove(o)
            except FileNotFoundError:
                pass

    def test_non_macro_code_is_unchanged(self):
        path = settings.ROOT_PATH + '/test/resources/module_sample.pyx.cm'
        o = settings.ROOT_PATH + '/test/resources/module_sample.pyx'

        try:
            expander = cm.FileExpander.from_path(path, o)
            expander()

            with open(path, 'r+') as f:
                prototype_content = f.read()

            self.assertTrue(os.path.exists(o), 'Out file was not created.')
            with open(o, 'r+') as f:
                # split off header lines and ignore them
                *_, new_content = f.read().split('\n', N_HDR)

            try:
                self.assertEqual(prototype_content, new_content)
            except AssertionError:
                # give some debug info
                proto_lines = prototype_content.split('\n')
                new_lines = new_content.split('\n')

                for proto_line, new_line in zip(proto_lines, new_lines):
                    if proto_line != new_line:
                        print('lines do not match:\n{}\n{}'
                              .format(proto_line, new_line))
                        break
                raise
        finally:
            try:
                os.remove(o)
            except FileNotFoundError:
                pass


class TestExtensionExpander(TestCase):

    ext_test_path = TEST_RESOURCES_PATH + '/ext_test'

    def tearDown(self):
        """
        Remove generated files between tests
        :return: None
        """
        for name in 'src.pxd', 'src.pyx':
            path = self.ext_test_path + '/' + name
            if os.path.exists(path):
                os.remove(path)

    def test_macro_definition_is_found(self):
        ext = Extension(
            name='foo',
            sources=[self.ext_test_path + '/src.pyx.cm'],
            extra_compile_args=["-ffast-math", "-Ofast"]  # misc args
        )

        ext_expander = cm.ExtensionExpander(ext)
        ext_expander()

        o1 = self.ext_test_path + '/src.pyx'
        o2 = self.ext_test_path + '/src.pxd'

        self.assertTrue(os.path.exists(o1), 'src.pyx was not created.')
        self.assertTrue(os.path.exists(o2), 'src.pxd was not created.')

        self.assertIn('TEST_VALUE', ext_expander.definitions)
        self.assertEqual('1234', ext_expander.definitions['TEST_VALUE'].body)

    def test_macro_definition_is_used(self):
        ext = Extension(
            name='foo',
            sources=[self.ext_test_path + '/src.pyx.cm'],
            extra_compile_args=["-ffast-math", "-Ofast"]  # misc args
        )

        ext_expander = cm.ExtensionExpander(ext)
        ext_expander()

        o1 = self.ext_test_path + '/src.pyx'
        o2 = self.ext_test_path + '/src.pxd'

        self.assertTrue(os.path.exists(o1), 'src.pyx was not created.')
        self.assertTrue(os.path.exists(o2), 'src.pxd was not created.')

        with open(o1, 'r+') as f:
            lines = f.readlines()
            self.assertEqual('1234\n', lines[4 + N_HDR])

    def test_ext_expander_modifies_source_paths(self):
        ext = Extension(
            name='foo',
            sources=[self.ext_test_path + '/src.pyx.cm'],
            extra_compile_args=["-ffast-math", "-Ofast"]  # misc args
        )

        ext_expander = cm.ExtensionExpander(ext)
        ext_expander()

        expanded_src = self.ext_test_path + '/src.pyx'

        self.assertEqual(expanded_src, ext.sources[0])

    def test_ext_expander_clean_method_removes_produced_files(self):
        ext = Extension(
            name='foo',
            sources=[self.ext_test_path + '/src.pyx.cm'],
            extra_compile_args=["-ffast-math", "-Ofast"]  # misc args
        )

        ext_expander = cm.ExtensionExpander(ext)
        ext_expander()

        o1 = self.ext_test_path + '/src.pyx'
        o2 = self.ext_test_path + '/src.pxd'

        self.assertTrue(os.path.exists(o1), 'src.pyx was not created.')
        self.assertTrue(os.path.exists(o2), 'src.pxd was not created.')

        ext_expander.clean()

        self.assertFalse(os.path.exists(o1), 'src.pyx was not cleaned.')
        self.assertFalse(os.path.exists(o2), 'src.pxd was not cleaned.')
