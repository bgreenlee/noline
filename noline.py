import sublime
import sublime_plugin
import re

class NolineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # get selected regions, or if none, the whole page
        non_empty_regions = [region for region in self.view.sel() if not region.empty()]
        self.regions = non_empty_regions or [sublime.Region(0, self.view.size())]

    def transform_regions(self, edit, search, replacement):
        for region in self.regions:
            text = self.view.substr(region)
            self.view.replace(edit, region, re.sub(search, replacement, text))

    def remove_linebreaks(self, edit):
        self.transform_regions(edit, r'[\r\n]', '')

    def remove_empty_lines(self, edit):
        self.transform_regions(edit, r'([\r\n])+', r'\1')

    def remove_whitespace_before_paragraphs(self, edit):
        self.transform_regions(edit, r'([\r\n]{2})[ \t]+', r'\1')

    def collapse_multiple_spaces(self, edit):
        self.transform_regions(edit, r'([ \t])+', r'\1')

class RemoveLinebreaks(NolineCommand):
    def run(self, edit):
        super(RemoveLinebreaks, self).run(edit)
        self.remove_linebreaks(edit)

class RemoveEmptyLines(NolineCommand):
    def run(self, edit):
        super(RemoveEmptyLines, self).run(edit)
        self.remove_empty_lines(edit)

class RemoveWhitespaceBeforeParagraphs(NolineCommand):
    def run(self, edit):
        super(RemoveWhitespaceBeforeParagraphs, self).run(edit)
        self.remove_whitespace_before_paragraphs(edit)

class CollapseMultipleSpaces(NolineCommand):
    def run(self, edit):
        super(CollapseMultipleSpaces, self).run(edit)
        self.collapse_multiple_spaces(edit)

class Blammo(NolineCommand):
    def run(self, edit):
        super(Blammo, self).run(edit)
        self.remove_whitespace_before_paragraphs(edit)
        self.collapse_multiple_spaces(edit)
        self.remove_linebreaks(edit)
