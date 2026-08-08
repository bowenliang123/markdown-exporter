from test_base import TestBase


class TestMdToJira(TestBase):
    def test_md_to_jira(self):
        # Define input path
        input_file = "test/resources/example_md.md"

        # Run the tool using the base class method and capture output
        result = self.run_script_with_output("parser/cli_md_to_jira.py", input_file)

        # Verify the output is not empty
        self.assertNotEqual(result.stdout.strip(), "", "Output is empty")

        # Verify Jira wiki markup syntax is present
        self.assertIn("h1.", result.stdout)
        self.assertIn("h2.", result.stdout)
        self.assertIn("||", result.stdout)
