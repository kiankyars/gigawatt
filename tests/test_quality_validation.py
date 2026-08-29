import unittest
from unittest.mock import patch

from gigawatt import validate


class QualityArtifactValidationTests(unittest.TestCase):
    def test_validator_rejects_stale_quality_artifacts(self) -> None:
        with (
            patch.object(
                validate.quality_pipeline,
                "build_artifacts",
                return_value=("stale\n", "stale\n", "test-digest"),
            ),
            self.assertRaisesRegex(
                validate.ValidationError,
                "course_quality.json is stale",
            ),
        ):
            validate.validate_project()


if __name__ == "__main__":
    unittest.main()
